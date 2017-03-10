import tail

def OnTailText(txt):
    print "-------------------"
    print txt

t = tail.Tail("/home/mayao/code/1.txt")
t.register_callback(OnTailText)
t.follow()

