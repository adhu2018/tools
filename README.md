# tools

- 支持了直接 `import tools` 的使用方法。例如：

  ```python
  import tools

  print(tools.md5(1))  # c4ca4238a0b923820dcc509a6f75849b
  print(tools.md5("1"))  # c4ca4238a0b923820dcc509a6f75849b
  ```

- 当只需要其中的某个功能时，可以直接下载对应的文件使用。例如：
  1. 下载 `md5.py` 
  2. 
      ```python
      import md5

      print(md5(1))  # c4ca4238a0b923820dcc509a6f75849b
      print(md5("1"))  # c4ca4238a0b923820dcc509a6f75849b
      ```
  3. 注意，有的模块中调用了其他模块，下载放在同一目录即可：
      - 使用 `download.py` 需要下载 `md5.py`
      - 使用 `meiriyiwen.py` 需要下载 `download.py` , `md5.py`
