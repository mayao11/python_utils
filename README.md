# python_utils
Some useful tools. Upload here to save.

## tail
  It is rewritten from kasun/python-tail, but changed a lot.
  
  It used pyinotify to drive the event loop, NOT sleep&check. The point is monitering the parent directory of the file, so you can get the event when the file move or change. When it does, you can just wait the file to recreate.
  
  It is only 100 lines of code. By a little familier with inotify(Linux file-change-notify function), You can easily change the code to fit your requirement.
