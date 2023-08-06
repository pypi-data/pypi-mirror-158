/*
    WinAPY - Windows API wrapper in C developed for Python.
    Copyright (c) 2022 Itzsten
*/

#include "utils.h"

#pragma comment(lib, "Shell32.lib")


static PyObject* PyCommandLineToArgvW(PyObject* _, PyObject* args) {
    WCHAR* cmdLine;
    if (!PyArg_ParseTuple(args, "u", &cmdLine)) return NULL;

    int argc;
    LPCWSTR* argv = CommandLineToArgvW(cmdLine, &argc);
    if (!argc) return Py_BuildValue("s", "");

    PyObject* arr = PyTuple_New(argc);

    for (INT i = 0; i < argc; i++) {
        PyTuple_SET_ITEM(arr, i, Py_BuildValue("u", argv[i]));
    }

    return Py_BuildValue("O", arr);
}
static PyObject* PyExtractIconA(PyObject* _, PyObject* args) {
    HINSTANCE hinst;
    LPCSTR name;
    UINT index;
    if (!PyArg_ParseTuple(args, "LsI", &hinst, &name, &index)) return NULL;
    HICON hic = ExtractIconA(hinst, name, index);
    if (hic == 1) {
        PyErr_SetString(PyExc_ValueError, "The file specified must be an executable, DLL, or icon file.");
        return NULL;
    }
    if (hic == NULL) {
        PyErr_SetString(PyExc_ValueError, "No icons were found in the specified file.");
        return NULL;
    }
    return Py_BuildValue("L", hic);
}
static PyObject* PyExtractIconW(PyObject* _, PyObject* args) {
    HINSTANCE hinst;
    LPCWSTR name;
    UINT index;
    if (!PyArg_ParseTuple(args, "LuI", &hinst, &name, &index)) return NULL;
    HICON hic = ExtractIconW(hinst, name, index);
    if (hic == 1) {
        PyErr_SetString(PyExc_ValueError, "The file specified must be an executable, DLL, or icon file.");
        return NULL;
    }
    if (hic == NULL) {
        PyErr_SetString(PyExc_ValueError, "No icons were found in the specified file.");
        return NULL;
    }
    return Py_BuildValue("L", hic);
}

static PyObject* PyShellExecuteA(PyObject* _, PyObject* args) {
    PyObject* obHwnd;
    PyObject* obOperation;
    LPSTR lpFile;
    PyObject* obParameters;
    PyObject* obDirectory;
    INT nShowCmd;

    HWND hwnd = NULL;
    LPSTR operation = NULL;
    LPSTR parameters = NULL;
    LPSTR directory = NULL;

    if (!PyArg_ParseTuple(args, "OOsOOi", &obHwnd, &obOperation, &lpFile, &obParameters, &obDirectory, &nShowCmd)) return NULL;

    if (obHwnd != Py_None) hwnd = PyLong_AsLong(obHwnd);
    if (obOperation != Py_None) operation = PyString_ToCharArr(obOperation);
    if (obParameters != Py_None) parameters = PyString_ToCharArr(obParameters);
    if (obDirectory != Py_None) directory = PyString_ToCharArr(obDirectory);

    HINSTANCE res = ShellExecuteA(hwnd, operation, lpFile, parameters, directory, nShowCmd);
    if (RaiseExceptionCheck(res < 32)) return NULL;
    return Py_BuildValue("L", res);
}
static PyObject* PyShellExecuteW(PyObject* _, PyObject* args) {
    PyObject* obHwnd;
    PyObject* obOperation;
    LPWSTR lpFile;
    PyObject* obParameters;
    PyObject* obDirectory;
    INT nShowCmd;

    HWND hwnd = NULL;
    LPWSTR operation = NULL;
    LPWSTR parameters = NULL;
    LPWSTR directory = NULL;

    if (!PyArg_ParseTuple(args, "OOuOOi", &obHwnd, &obOperation, &lpFile, &obParameters, &obDirectory, &nShowCmd)) return NULL;

    if (obHwnd != Py_None) hwnd = PyLong_AsLong(obHwnd);
    if (obOperation != Py_None) operation = PyUnicode_AsWideCharString(obOperation, NULL);
    if (obParameters != Py_None) parameters = PyUnicode_AsWideCharString(obParameters, NULL);
    if (obDirectory != Py_None) directory = PyUnicode_AsWideCharString(obDirectory, NULL);

    HINSTANCE res = ShellExecuteW(hwnd, operation, lpFile, parameters, directory, nShowCmd);
    if (RaiseExceptionCheck(res < 32)) return NULL;
    return Py_BuildValue("L", res);
}
static PyObject* PySHQueryRecycleBinW(PyObject* _, PyObject* args) {
    LPWSTR rootPath = NULL;
    PyObject* obRootPath;
    if (!PyArg_ParseTuple(args, "O", &obRootPath)) return NULL;

    if (obRootPath != Py_None) rootPath = PyUnicode_AsWideCharString(obRootPath, NULL);

    SHQUERYRBINFO bin;
    bin.cbSize = sizeof(SHQUERYRBINFO);

    if (ExceptionCheckHRESULT(SHQueryRecycleBinW(rootPath, &bin))) return NULL;

    return Py_BuildValue("(LL)", bin.i64Size, bin.i64NumItems);
}
static PyObject* PySHQueryRecycleBinA(PyObject* _, PyObject* args) {
    LPSTR rootPath = NULL;
    PyObject* obRootPath;
    if (!PyArg_ParseTuple(args, "O", &obRootPath)) return NULL;

    if (obRootPath != Py_None) rootPath = PyString_ToCharArr(obRootPath);

    SHQUERYRBINFO bin;
    bin.cbSize = sizeof(SHQUERYRBINFO);

    if (ExceptionCheckHRESULT(SHQueryRecycleBinA(rootPath, &bin))) return NULL;

    return Py_BuildValue("(LL)", bin.i64Size, bin.i64NumItems);
}
static PyObject* PySHEmptyRecycleBinA(PyObject* _, PyObject* args) {
    PyObject* obHwnd;
    PyObject* obPath;
    LPCSTR path = NULL;
    HWND hwnd = NULL;
    DWORD dwFlags;
    if (!PyArg_ParseTuple(args, "OOk", &obHwnd, &obPath, &dwFlags)) return NULL;
    if (obHwnd != Py_None) hwnd = PyLong_AsLong(obHwnd);
    if (obPath != Py_None) path = PyString_ToCharArr(obPath);
    HRESULT res = SHEmptyRecycleBinA(hwnd, path, dwFlags);
    if (HRESULT_CODE(res) == 0xFFFF) {
        PyErr_SetString(PyExc_FileNotFoundError, "The recycle bin is empty or unavailable on the specified drive.");
        return NULL;
    }
    if (ExceptionCheckHRESULT(res)) return NULL;
    return Py_BuildValue("i", 0);
}
static PyObject* PySHEmptyRecycleBinW(PyObject* _, PyObject* args) {
    PyObject* obHwnd;
    PyObject* obPath;
    LPCWSTR path = NULL;
    HWND hwnd = NULL;
    DWORD dwFlags;
    if (!PyArg_ParseTuple(args, "OOk", &obHwnd, &obPath, &dwFlags)) return NULL;
    if (obHwnd != Py_None) hwnd = PyLong_AsLong(obHwnd);
    if (obPath != Py_None) path = PyUnicode_AsWideCharString(obPath, NULL);
    HRESULT res = SHEmptyRecycleBinW(hwnd, path, dwFlags);
    if (HRESULT_CODE(res) == 0xFFFF) {
        PyErr_SetString(PyExc_FileNotFoundError, "The recycle bin is empty or unavailable on the specified drive.");
        return NULL;
    }
    if (ExceptionCheckHRESULT(res)) return NULL;
    return Py_BuildValue("i", 0);
}
static PyObject* PyShellAboutA(PyObject* _, PyObject* args) {
    PyObject* obHwnd;
    PyObject* obOtherStuff;
    PyObject* hicon;
    LPCSTR szApp;
    LPCSTR szOtherStuff = NULL;
    HICON icon = NULL;
    HWND hwnd = NULL;
    if (!PyArg_ParseTuple(args, "OsOO", &obHwnd, &szApp, &obOtherStuff, &hicon)) return NULL;
    if (obHwnd != Py_None) hwnd = PyLong_AsLong(obHwnd);
    if (obOtherStuff != Py_None) szOtherStuff = PyString_ToCharArr(obOtherStuff);
    if (hicon != Py_None) icon = PyLong_AsLongLong(hicon);

    BOOL res = ShellAboutA(hwnd, szApp, szOtherStuff, icon);
    if (!res) {
        PyErr_SetString(PyExc_OSError, "ShellAboutA failed");
        return NULL;
    }
    return Py_BuildValue("i", 0);
}
static PyObject* PyShellAboutW(PyObject* _, PyObject* args) {
    PyObject* obHwnd;
    PyObject* obOtherStuff;
    PyObject* hicon;
    LPCWSTR szApp;
    LPCWSTR szOtherStuff = NULL;
    HICON icon = NULL;
    HWND hwnd = NULL;
    if (!PyArg_ParseTuple(args, "OuOO", &obHwnd, &szApp, &obOtherStuff, &hicon)) return NULL;
    if (obHwnd != Py_None) hwnd = PyLong_AsLong(obHwnd);
    if (obOtherStuff != Py_None) szOtherStuff = PyUnicode_AsWideCharString(obOtherStuff, NULL);
    if (hicon != Py_None) icon = PyLong_AsLongLong(hicon);

    BOOL res = ShellAboutW(hwnd, szApp, szOtherStuff, icon);
    if (!res) {
        PyErr_SetString(PyExc_OSError, "ShellAboutW failed");
        return NULL;
    }
    return Py_BuildValue("i", 0);
}

static PyMethodDef module_methods[] = {
    { "ShellAbout",  PyShellAboutW, METH_VARARGS },
    { "ShellAboutW", PyShellAboutW, METH_VARARGS },
    { "ShellAboutA", PyShellAboutA, METH_VARARGS },
    { "SHEmptyRecycleBin",  PySHEmptyRecycleBinW, METH_VARARGS },
    { "SHEmptyRecycleBinW", PySHEmptyRecycleBinW, METH_VARARGS },
    { "SHEmptyRecycleBinA", PySHEmptyRecycleBinA, METH_VARARGS },
    { "SHQueryRecycleBin",  PySHQueryRecycleBinW, METH_VARARGS },
    { "SHQueryRecycleBinW", PySHQueryRecycleBinW, METH_VARARGS },
    { "SHQueryRecycleBinA", PySHQueryRecycleBinA, METH_VARARGS },
    { "ShellExecute",  PyShellExecuteW, METH_VARARGS },
    { "ShellExecuteW", PyShellExecuteW, METH_VARARGS },
    { "ShellExecuteA", PyShellExecuteA, METH_VARARGS },
    { "CommandLineToArgvW", PyCommandLineToArgvW, METH_VARARGS },
    { "CommandLineToArgv",  PyCommandLineToArgvW, METH_VARARGS },
    { "ExtractIcon",  PyExtractIconW, METH_VARARGS },
    { "ExtractIconW", PyExtractIconW, METH_VARARGS },
    { "ExtractIconA", PyExtractIconA, METH_VARARGS },
    /* sentinel */
    { 0 }
};

static struct PyModuleDef ModuleCombinations =
{
    PyModuleDef_HEAD_INIT,
    "winapy_shell", /* name of module */
    NULL,
    -1,   /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    module_methods
};


void PyInit_winapy_shell(void) {
    PyModule_Create(&ModuleCombinations);
}