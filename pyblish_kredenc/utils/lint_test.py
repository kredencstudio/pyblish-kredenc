import filelink

src = 'P:/projects/filelink/test_file.mov'

for i in range(1000):
    dst = 'P:/projects/filelink/test_file_{}.mov'.format(i)
    filelink.create(src, dst, filelink.HARDLINK)
