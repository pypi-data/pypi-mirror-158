The Jigsaw Piece Maker
======================

A jigsaw puzzle pieces generator that levels the playing field.

Currently in use by `Puzzle Massive <http://puzzle.massive.xyz>`_ to create
puzzles with 5000+ pieces.

It creates jigsaw puzzle pieces in multiple formats: svg, jpg, and png.  The
number and size of pieces are set by passing the script different options.  It
takes a while to run if doing a lot of pieces.  Extra JSON files are created
with details on size of pieces and adjacent pieces information which is commonly
used when verifying that two pieces can join together.


Installing
----------

Requires:

Python Packages:

* `Pillow <http://github.com/python-imaging/Pillow>`_
* `pixsaw <http://github.com/jkenlooper/pixsaw>`_
* `beautifulsoup4 <http://www.crummy.com/software/BeautifulSoup/bs4/>`_
* `svgwrite <https://pypi.python.org/pypi/svgwrite>`_
* lxml
* `glue <https://github.com/jorgebastida/glue>`_ (Only partially included in
  piecemaker source)

Other Software needed:

* `potrace <http://potrace.sourceforge.net/>`_

If on ubuntu or other debian based distro::

    sudo apt-get --yes install libspatialindex6
    sudo apt-get --yes install optipng
    sudo apt-get --yes install python3-pil
    sudo apt-get --yes install potrace libffi-dev libxml2-dev python3-lxml python3-xcffib
    sudo apt-get --yes install librsvg2-bin
    sudo apt-get --yes install python3-pip


Install with pip in editable mode for developing and use virtualenv to isolate
python dependencies::

    python3 -m venv .
    source ./bin/activate
    pip install --upgrade --upgrade-strategy eager -e .


Usage
-----

See the script.py for more.  Not everything has been implemented. Use this
example command to create 100 randomly generated jigsaw puzzle pieces from
test.jpg image. This assumes that the 'test' directory is empty since that is
where it will be placing all the generated files.  The test.jpg is the source
image that will be used when creating the pieces.  It is not modified.::

    piecemaker --dir test  --number-of-pieces 100 test.jpg


Docker Usage
------------

A Dockerfile also can be used to build an image and run it.::

    docker build -t piecemaker:latest .

    mkdir -p out/tmp
    cp test.jpg out/
    rm -rf out/tmp/*

    docker run -it --rm \
        --mount type=bind,src=$(pwd)/out,dst=/out \
        piecemaker:latest \
        piecemaker --dir /out/tmp --number-of-pieces 100 /out/test.jpg

