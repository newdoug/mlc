TODO now:

* Decide on format for data generation output. Make sure it's expandable for future.
* Run some of the analysis on some small amounts of data
* Write some unit tests for feature function/analysis
* Implement PQC functions


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
** Feature selection
** Data generation


* Feature selection thoughts:
*** Keep all feature information, but mark each feature as "good enough" or not
**** "Good enough" according to what?
**** List whsat feature selection methods say it was or wasn't good enough
**** Ensure the heuristic we used/gave to the feature selection method is tracked.
**** So that later we can re-calculate feature selection methods as more data is obtained and continue improving our model.


* Information to track:
** About plaintext:
*** Did we generate it?
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
      existence of strings and ocation(s) would be useful.
      * Keeping track of certain portions of files would probably be useful too.
        Especially first few bytes (where magic numbers/strings/values usually
        are). Magic elsewhere (in sub-structures, for example) wouldn't be as
        easily.
      * binwalk that recursively finds stuff may primarily look for magic. How
        would that work here?

* Maybe turn certain things or everything into services so that we can constantly be generating and/or obtaining data
  and running it through the pipeline to other steps and constantly improving the model.
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
  * Initial interpretation of this question: Bit of plaintext (input) vs bit of
    ciphertext (output).
  * Another interpretation: Bit of key vs bit of output. Bit of output could be:
    entire ciphertext? Or a single block (in the case of block ciphers) or bit
    of something else for stream ciphers?
* Make linters as git precommit hooks
  * Other precommit hooks? Can probably use some precommit library if desired.

* See how audio matching machine learning/matching works. Find patterns in
  waveform and matches them up with input test signal? Could be useful for
  feature creation and/or pattern determination on ciphertexts.
* Add an "auto-break" flag once it has a guess at what the input looks like. If
  the result is some kind of cipher. If it's some breakable cipher like shift,
  Caesar, substitution, etc., it'll be easy, otherwise, probably just brute
  force unless we come up with full crypto breaking methods for that cipher
  (i.e., not just brute force).
* Identify test (SMS) messages. Emojis? Acronyms used in texting Text message
  "format" e.g. how they may be stored on phones with a header and/or footer or
  how they're sent over the air with header or footer.
* Identify if it's an over-the-air message? Psk encoding identification? Common footers and headers?
* Identify packet formats. Ethernet, tcp, ftp, udp, IP, etc.
* Turn the jobs thing from mlc into generic multi-processing ability. Kinda already done.
* Make the jobs thing support multiple communication methods. Tcp socket, udp socket, SSH, Unix socket, something more inter-process specific, etc.
* Try to identify more complex meanings behind tars/archives. This can mean at least 2 things:
  1) "the contents of this tar looks like a got repo" or something similar
  2) "this exact file is available here: *some Internet link*" or "this exact file is available on this website somewhere: *some website name and/or link" or "a very similar file (maybe show/offer a diff if possible and available) is available here: *some link or site name*" (that one sounds a bit difficult and would probably take a ton of processing - would need to keep track of all files we've seen and metadata about it and then compare each of them to this one were currently inspecting - begs the idea of a service with background tasks/sub services/jobs running and sending notifications in some way to the user), or "this archive contains a git repo (commit XXXX if possible) that's from here: *repo link (GitHub, gitlab, bitbucket, another site, etc.)*"
* Average difference between bytes of plaintext and ciphertext
  * Same thing, but shift each byte's index by 1, 2, 3, ... (e.g., compare byte 0 or plaintext with byte 1 of
    ciphertext)
* Average bytes similar (e.g., within X%) between plaintext and ciphertext
* String similarity/substring algorithms popular in CS classes, but used on ciphertext
* Make a generic pattern finding algorithm on integer sequences/series. Then, apply to these ciphertexts
* Average 16-bit sum, 24-bit, 32-bit, etc. Average block sum
* Consider `tabular` package for displaying data in ASCII-like tables.
* Dot products
* Cross products
* More matrix math
* Similarity ranges between plaintext and ciphertext, not just exact byte matches, but also just almost equal (varying
  "almost" measures)
* Ratio of similarity between blocks of plaintext and ciphertext. I.e., is there any relationship between (block 1 of PT
  / block 2 of PT) and (block 1 of CT / block 2 of CT). Probably try some different variations on this too.


* Determine common ways that keys are generated:
  * Randomly
    * In the symmetric + asymmetric (to transfer symm key) methodology, symm key can usually be completely randomly generated.
    * What's the source of randomness? Can that be broken? Can the seed(s) be easily replicated? How big is the space
      for seeds (is it just a 32-bit int? Is that just put through an algorithm to generate a larger key?) It's probably
      better than that, but maybe whatever is currently used is still imperfect an exploitable. E.g., even if the seed
      to generate the key is based on several environmental/HW-related factors that's rather large (maybe 64 >= bytes),
      what is the *effective* key space? Maybe one of the factors that goes into the 64 bytes (say, 8 bytes) effectively
      only has about 4 bytes of possible values and maybe even only 2-3 types of likely possible values. Apply that to
      the other factors and maybe the space is much smaller than thought.
      * In this case, generate all possible inputs (or possibly just the most likely ones since it's probably still a
        very large key space) and generate the hashes/PBKDF/whatever that would be used on it.
  * User password
    * Often salted, sometimes and/or pepper too/instead which is probably random.
      * Depends on how big the salt is, but classic brute force with hash-table style stuff may be sufficient.
    * If unsalted, the classic brute force with hash-table style stuff would probably be sufficient.
    * In either case (salted or unsalted), need to know the most commonly used hash methods. SHA256? MD5? PBKDF-style?
      etc.
  * Find data set online containing all known collisions for each hash type.
  * Find existing hash tables online to reduce re-computation.
    * Create own service that hosts such data. Allow:
      * Display of all columns + small (<100, say) sample of the data.
      * Various hash types
      * Various KDF types
      * Various PBKDF types
      * Allow computation submits by users. E.g., get all <WEIRD_HASH_TYPE> for all values of length X bits. Server will
        compute them all, save them in case someone in future wants them, and gives them for download. If it'll take a
        while, give the user a download link that, once computation is complete, will return the results. Could also
        accept their email and say we'll send them an email with the download link once it's complete. This would preent
        allowing users to spam the download link.
        * Similarly, offer users to provide code that implements a hash algorithm. They must list third-party packages
          required. We will accept it, offer them thanks, and tell them we'll manually inspect the code ourselves and if
          it's valid and better (faster) than the current implementation, we'll use it. Only accept certain languages,
          probably just C, C++, Python2, Python3.
      * Selection of which columns the user wants to download.
      * Provide this via a Python API, free download, stream/generator-like data download.
    * Also post my own.


Permute actual code pulled from GitHub or something using lexer/parser to come up with variations of algorithms and see if any produce any keys or partial keys or offsets of keys or something at all related to a key
Permuting C/c++ and assembly.
Start with something similar to the actual algorithm.
Also try bad transformations to see if anything easy somehow works
Aes, chacha20, rsa, etc.

Idea if not already mentioned above: If we can get any kind of information about what the plaintext is underneath a
given ciphertext, it could make other attacks more feasible like chosen plaintext or simply brute forcing keys (can at
least verify if any blocks *might* have successfully been decrypted (if looks like the right kind of plaintext we
determined)).


# Commands

## Install `poetry`

```
# Or some other install command, e.g., with `apt` or `yum`
curl -sSL https://install.python-poetry.org | python3 -
# Add this line to `~/.bashrc`: update PATH to make poetry runnable (it'll probably be put into ~/.local/bin)
export PATH="$PATH:$HOME/.local/bin"
source ~/.bashrc
```

## Create a project and install dependencies

Assumes you're in the same directory as `pyproject.toml` (the primary repo dir).

```
poetry install
```

## Enter Virtual Environment

After installing above, enter the virtual environment that was created.

```
# env activate will just print the command necessary to activate the environment
$(poetry env activate | head -n1)
```

or alternatively just source the `env_activate.sh` script:

```
source env_activate.sh
```

## Install pre-commit Hooks

```
pre-commit install
```

### Run pre-commit Hooks

Runs the pre-commit hooks manually.

```
pre-commit run --all-files
```

## Format Code

This is the command to manually run the code formatting on current directory. Code formatting should automatically take
place as part of a pre-commit hook.
```
poetry run black .
```

## Run Tests

```
poetry run pytest
```

## Adding pip packages after install

Packages that aren't in the pyproject.toml that you just want one-off installed.

```
poetry self add <package_name>
```

If you want them to be added to `pyptoject.toml`:
```
poetry add <package_name>
```
