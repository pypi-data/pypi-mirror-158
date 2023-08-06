Clock Widgets for Kivy
======================

[![Github Build Status](https://github.com/ebs-universe/kivy_garden.ebs.clocks/workflows/Garden%20flower/badge.svg)](https://github.com/ebs-universe/kivy_garden.ebs.clocks/actions)

This package provides relatively simple Clock widgets for Kivy. 

Presently it has only a single and trivial clock and is certainly not deserving 
of a whole package. In time, this package is intended to hold a curated 
collection of clocks in both Python and .kv.  

The presently included widgets are easily implemented from scratch in both 
Python and Kv, and for most non-EBS applications, you'd probably just want 
to roll your own or use some .kv based clock widget available in the wild.
The typical EBS application can get unwieldy pretty quickly though, so this
package affords a separation of concerns which aids in maintainability.

If you are looking for something you can just pip install and which just works, 
and don't care that it might be written in python and might pull in additional 
dependencies, then this might be an option.

Included clock widgets : 
  
  - SimpleDigitalClock

No clock which have its own kivy_garden package will be added to this collection,
and the collection itself will grow (very) slowly.

This package is part of the EBS widget collection for Kivy. It is written in 
mostly Python and depends on the EBS core widgets and widget infrastructure package. 
For more information, see [kivy_garden.ebs.core](https://github.com/ebs-universe/kivy_garden.ebs.core)

See https://kivy-garden.github.io/ebs.flower/ for the rendered flower docs.

Please see the garden [instructions](https://kivy-garden.github.io) for 
how to use kivy garden flowers.


CI
--

Every push or pull request run the [GitHub Action](https://github.com/kivy-garden/flower/actions) CI.
It tests the code on various OS and also generates wheels that can be released on PyPI upon a
tag. Docs are also generated and uploaded to the repo as well as artifacts of the CI.


TODO
-------

* add your code

Contributing
--------------

Check out our [contribution guide](CONTRIBUTING.md) and feel free to improve the flower.

License
---------

This software is released under the terms of the MIT License.
Please see the [LICENSE.txt](LICENSE.txt) file.

How to release
===============

See the garden [instructions](https://kivy-garden.github.io/#makingareleaseforyourflower) for how to make a new release.
