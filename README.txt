Concept:

* Basic steps:
** Generate/get lots of plaintext data
** Encrypt it and track information about data.
*** Optionally compress instead of encrypt
*** Optionally compress and *then* encrypt
**** Basically the same entire problem, but given compressed bytes instead of
ciphertext
** Calculate a lot of features on the data
** Feature selection
** Run features through model to train (traditioanlly split input data into testing data (~15%ish) ad training data (~85%ish))
** (Optionally, just to see how the model is performing): run on new data to see how accurate it is
*** "Run" as in make it try to guess various things about the data, not just the key or cipher type
*** We likely should use different models and different feature selection methods for each thing we're attempting to guess


Components:

* Data generator
* Feature calculator
* Feature selection
* Model trainer and tester
* Classifier


* Things to multiprocess/distribute processing of:
** Generate feature calculation
** Model training
** Everything, but for each thing we're trying to guess (e.g., one machine for one thing we're trying to guess (one machine for file type, one machine for cipher type, etc.), but probably more than 1 machine for each if we're getting serious).
** Fetaure selection
** Data generation


* Feature selection thoughts:
*** Keep all feature information, but mark each feature as "good enough" or not
**** "Good enough" according to what?
**** List whsat feature selection methods say it was or wasn't good enough
**** Ensure the heuristic we used/gave to the feature selection method is tracked.
**** So that later we can re-calculate feature selection methods as more data is obtained and continue improving our model.


* Information to track:
** About plaintext:
*** Did we geerate it?
*** What kind of data is it? (see below for types of data/files)
*** Where is it from if we didn't generate it? In general, source = ?
** About ciphertext
*** To track:
**** Original plaintext
**** Ciphertext
**** If a nonce was used
***** What the nonce was if so
**** If a IV was used
***** What the IV was if so
**** Key size
**** Key
**** The cipher
**** The crypto library used - implementation could matter slightly in some cases (maybe just for randomness/seeding, but maybe for other stuff too, IDK)?
**** Entropy source
***** srand and rand?
***** seed? if possible
***** /dev/urandom?
***** /dev/random?
***** Windows GenRandom or whatever? Not sure what to do here if we're running on Linux primarily.
****** Maybe can write a data generation portion to run on Windows and store data so the rest can run on Linux
**** OS information? (Could impact randomness?)
***** Optional
**** Local system time? Remote time probably doesn't really matter.
***** If so, maybe try data generation/encryption runs on machines where we spoof the time.

* Generate or obtain lots of plaintext data of different varieties.
** Random binary
** Random ASCII
** Sparse random ASCII
** Sparse random binary
** Common file types - see below
*** Likely need to borrow some from other sources and may need to worry about copyright stuff?
*** Some will require large amounts of storage, like videos
* NOTE: maybe do something extremely similar, but just on the plaintext.
  Basically the whole process including good feature determination. At lesat a
  couple of reasons:
  * If the ML model learns what things about the plaintext are important, then
    maybe the same or similar (possibly just shifted or maybe some linear or
    noticeable transformation) would apply to the ciphertext somehow.
      * TODO: some way to automate detecting this? Imagine what a human might do
        when looking at it and trying to find similarities.
        * If even one case turns up, could break the crypto.
  * Could be a useful enough application by itself.
    * Could easily turn it into a website (don't keep data stored in case it's
      something illegal) with ads or some other monetization scheme - make some money.
    * If developing it, running "strings" on input and taking note and/or
      existance of strings and ocation(s) would be useful.
      * Keeping track of certain portions of files would probably be useful too.
        Especially first few bytes (where magic numbers/strings/values usually
        are). Magic elsewhere (in sub-structures, for example) wouldn't be as
        easily.
      * binwalk that recursively finds stuff may primarily look for magic. How
        would that work here?

* Maybe turn certain things or everything into services so that we can constantly be generating and/or obtaining data and running it trough the pipeline to other steps and constantly improving the model.
** Being able to use the model for classification while submitting training data?


Things to determine/guess based on ciphertext:
* File type (see below: Video file? Audio file? Plaintext ASCII? Source code? Compressed file? Uncompresesd archive? Etc.)
* Cipher type
* Key size
* Nonce used?
* IV used?
* AEAD?
* Is it just a hash?
* Hash type? (obviously is much easier to guess given the size, but assume
  that's not necessarily the tell - maybe even train on substrings or on
  concatenated hashes)
** Same for CRCs and checksums
** In future: could have a secondary computation lookup thing to lookup in table
to see if it's a known hash.
*** Similar for CRC's, checksums, etc. Especially since those are more likely to
be duplicated. If given one, can return all known source bytes so user can maybe
see if any look especially useful.
* ECCs
** Reed-solomon
* Is it a MAC?
* MAC type?
* Digital signatures
* Compression algorithm
* The key itself - big if true
* If not the actual key, perhaps some range information about the key. E.g., "first 32 bits of key are between X and Y" or "the entire key is between X and Y"

* Do all feature calculations on:
** Just ciphertext/input
** Various transformations (configurable) on the ciphertext/input
*** An attempted decryption (sometimes it can complete even if incorrectly, depending on the cipher)
*** Various XOR and other simple math-y operations
**** Linear
*** Some transformations similar to decryption, but maybe only 1 or a couple steps
**** Mostly non-linear
**** Can borrow these from various existing ciphers.

* For some high-level API, if failing to determine what it is, run through `file`, `binwalk`, etc. in case its not really ciphertext


** File types (to try to guess for only given ciphertext):
*** Various compression file formats
**** Examples:
***** gzip
***** 7zip
***** rar
***** zip
***** lzma
***** bz2
***** zlib
***** tar archive (uncompressed)
***** tar archive (compressed)
*** Various other file types:
**** base64
**** JSON
**** YAML
****
*** Video file types
**** Examples:
***** mp4
***** mkv
***** mpeg
***** flv
***** etc.
**** Pull from YouTube, vimeo, etc.
*** Audio file types
**** Examples:
***** mp3
***** flac
***** wav
***** etc.
*** Executable file types
**** Examples:
***** exe
***** dll
***** elf
***** .so
***** .a
***** .lib
***** .o
*** Plaintext source code files
**** Examples:
***** C
***** C++
***** Python
***** Java
***** Perl
***** Bash/shell
**** Pull lots from GitHub and elsewhere
*** Document file types
**** Examples:
***** doc
***** docx
***** pdf
***** markdown
***** asciidoc
***** rtf
***** epub
***** mobi


Ideas:

* Probably written in C/C++
** Faster than Python
*** Can still write a Python layer later.
** Multiprocessing might actually be easier because of that weird deadlocking issue.


* Distributed computing

** For data work
*** Feature calculation

** For ML work
*** Model training
*** Data classification

** Maybe come up with simple custom distributed computation solution? Just an init stage (SSH in, put the code in place, ensure dependencies are installed, etc.), then "set up comms" stage (set up sockets/server, start up services/applications)


* Database

** Local initially, remote eventually.
*** Use ORM or at least a middleware/adapter class.

** Spark?
*** Not sure if super good distributed processing support.
** Hadoop?
*** Not sure yet if Python API exists. Sahara?


# TODO

* More comprehensive unit tests
** More unit tests in general - some things aren't unit tested at all
* More algorithms to finish implementing
** Hashing algs
** CRC algs
** Checksum algs
* Define `__all__` more consistently for everyone
* Run linters and resolve issues
* CI/CD - run tests in GH job(s)?
* Distribute processing across actual nodes (AWS, etc.)

* Feedback back into itself?
** If it can, with reasonable confidence, determine part of a ciphertext to be
some plaintext, then use that info to try to determine the rest and add that
learning to the model.
* Learn with keys too. E.g., use key attributes/features as part of the learning
  model. May be able to determine certain sets of bits of the key at least.
* Does every bit of input affect every bit of output? To what degree? If not, then we can brute force only certain bits (with known plaintext).
  * Initial interpretation of this quesiton: Bit of plaintext (input) vs bit of
    ciphertext (output).
  * Another interpretation: Bit of key vs bit of output. Bit of output could be:
    entire ciphertext? Or a single block (in the case of block ciphers) or bit
    of something else for stream ciphers?
* Make linters as git precommit hooks
  * Other precommit hooks? Can probably use some precommit library if desired.
