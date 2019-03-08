# Py Image Merger

Py Image Merger is a small tool to merge all images found (recursively)
in a folder into one image.


## How it works

It's a command-line utility.
4 parameters:
* "`-s`" / "`--src`": src directory where all image files are
* "`-d`" / "`--dst`": destination image file
* "`-w`" / "`--max-width`": max width of dst image file
* "`-b`" / "`--best-fit`": try to match closely 'width=height' of dst image file


## Usage samples

* *Windows* sample: search for all known image files (`gif`, `jpg`, `png`),
found in the directory `D:/UnityProjects/32x32 assets/Monsters` and put them
into one "big" file named `Monsters.png`, to a `max_width` of `1896`

    ```sh
    $ python3 merge_files.py \
    --src "D:/UnityProjects/32x32 assets/Monsters" \ 
    --dst "D:/UnityProjects/32x32 assets/Monsters.png" \
    -w 1896
    ```

* *Linux* sample: search for all known image files (`gif`, `jpg`, `png`),
found in the directory `/home/olivier/Monsters` and put them
into one "big" file named `Monsters.png`, and try to do as "square" image.
Note the `-q` option.

    ```sh
    $ python3 merge_files.py -q \
    --src "/home/olivier/Monsters" --dst "/home/olivier/Monsters.png"
    ```

## Who uses *Py Image Merger*

* [HQF Development (yes my company, I'm a freelance)](https://hqf.fr)
* Maybe other ones, but I'm the only one right now. If you've used it,
  let me know so I can add you here. That would be nice to know that I'm not
  working only for me!
 