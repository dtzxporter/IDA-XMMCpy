# IDA-XMMCpy
A plugin for IDA-Pro to copy XMMWORDs to usable C++ intrinsics.

## Installation
Just copy `ida_xmmcpy.py` and `ida_xmmcpy_ft.py` to the plugins folder and restart IDA.

## Usage
Select the XMMWORD you want to export, similar to using `Edit->Export Data` and instead, use `Edit->Plugins->XMMCpy` to convert it to an intrinsic for loading, it will also be copied to the clipboard.