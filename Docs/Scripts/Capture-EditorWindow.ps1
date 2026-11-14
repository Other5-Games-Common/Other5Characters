# Saves a PNG of one Unreal editor window (for the Creator guides' screenshots). It renders the window itself
# (PrintWindow), so other apps on top of it never end up in the picture.
#   .\Capture-EditorWindow.ps1 -Out ..\Images\AddingACharacter\02-FabPanel.png
#   .\Capture-EditorWindow.ps1 -Out x.png -Title 'IK_Gideon'   # a separate editor window, by part of its title
param(
	[Parameter(Mandatory)] [string] $Out,
	[string] $Title = '',
	[string] $Process = 'UnrealEditor'
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Text;
using System.Collections.Generic;
using System.Runtime.InteropServices;
public static class Other5Win {
	[StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
	public delegate bool EnumProc(IntPtr h, IntPtr p);
	[DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc f, IntPtr p);
	[DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
	[DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
	[DllImport("user32.dll", CharSet = CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
	[DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
	[DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint flags);
	[DllImport("user32.dll")] public static extern bool SetProcessDpiAwarenessContext(IntPtr v);
	public static List<IntPtr> Windows(uint pid) {
		var list = new List<IntPtr>();
		EnumWindows((h, p) => { uint w; GetWindowThreadProcessId(h, out w); if (w == pid && IsWindowVisible(h)) list.Add(h); return true; }, IntPtr.Zero);
		return list;
	}
	public static string Text(IntPtr h) { var s = new StringBuilder(512); GetWindowText(h, s, 512); return s.ToString(); }
}
'@
[Other5Win]::SetProcessDpiAwarenessContext([IntPtr](-4)) | Out-Null   # per-monitor v2, as the editor is
$p = Get-Process $Process | Where-Object MainWindowHandle -ne 0 | Select-Object -First 1
if (-not $p) { throw "No $Process window" }
$hwnd = $p.MainWindowHandle
if ($Title) {
	$hwnd = [Other5Win]::Windows([uint32]$p.Id) | Where-Object { [Other5Win]::Text($_) -like "*$Title*" } | Select-Object -First 1
	if (-not $hwnd) { throw "No $Process window titled *$Title*" }
}
$r = New-Object Other5Win+RECT
[Other5Win]::GetWindowRect($hwnd, [ref] $r) | Out-Null
$w = $r.Right - $r.Left; $h = $r.Bottom - $r.Top
$bmp = New-Object System.Drawing.Bitmap $w, $h
$g = [System.Drawing.Graphics]::FromImage($bmp)
$dc = $g.GetHdc()
[Other5Win]::PrintWindow($hwnd, $dc, 2) | Out-Null   # PW_RENDERFULLCONTENT
$g.ReleaseHdc($dc)
New-Item -ItemType Directory -Force (Split-Path -Parent ([IO.Path]::GetFullPath($Out))) | Out-Null
$bmp.Save([IO.Path]::GetFullPath($Out), [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
"Saved $Out ($w x $h)"
