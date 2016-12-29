# We already have some versions of python, but want some more...
cd ~/src

mkdir -p pypy
cd pypy
wget https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-5.0.1-linux_x86_64-portable.tar.bz2
tar --strip-components 1 -xvf pypy-5.0.1-linux_x86_64-portable.tar.bz2
cd ..

mkdir -p pypy3
cd pypy3
wget https://bitbucket.org/squeaky/portable-pypy/downloads/pypy3-2.4-linux_x86_64-portable.tar.bz2
tar --strip-components 1 -xvf pypy3-2.4-linux_x86_64-portable.tar.bz2
cd ..

mkdir -p ~/.local
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tar.xz
tar xvf Python-3.5.2.tar.xz
cd Python-3.5.2
./configure --prefix=/home/$USER/.local/
make
make install

# You actually need to put this line in the tests section. Not sure of a better solution.
# export PATH=$PATH:~/src/pypy3/bin:~/src/pypy/bin:~/.local/bin/
