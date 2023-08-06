
loz
==================================================
Command line password manager.

Why?
-------------------------
You may ask why is there a need for another open source password manager. Here are some features that most currently available password managers lack and that loz is focusing on:

- **Designed for command line.** Loz allows you to perform all tasks directly on the command line.
    - You can pipe the secrets out of it directly to files.
    - Bash completion is available for all commands and even domains/usernames.
    - Commands are entered directly without loading any custom loz console.

- **Asymmetric encryption.** Need to quickly add new entry or generate a password? No problem. With asymmetric encryption, you don't need to type your master password each time you add new entry. It even makes no sense to have to do that, right? You already know what you are entering.

- **Single file storage.** [Lozfile](#lozfile-and-encryption) contains all entries, secrets and encryption keys in a simple json format. You can just copy it over to another machine and continue where you left off.

Requirements
-------------------------
- Python >= 3.10

install
-------------------------
`pip install loz`

### setup bash completion
Add the following to your .bashrc or .profile:
```
eval "$(loz bash-completion)"
```

Alternatively generate bash completion file in a directory specific for your system,
e.g. for Debian, Ubuntu and Fedora:
```
loz bash-completion > sudo tee /etc/bash_completion.d/loz
```

usage
-------------------------

### Initialize lozfile

`loz init` - This is required first step that will generate storage file at default location `~/.loz`. If you want to use different location or separate storage file, you can specify that with `loz -f path/to/lozfile [COMMAND] [OPTIONS]`, but then you always need to include that switch when using other commands.

You will be asked to enter the master password which will be required for decrypting your secrets. Read more about the lozfile, what it contains, what is being encrypting and what it's always revealing in the [lozfile section](#lozfile-and-encryption) of this doc.

### Add secret

`loz add mydomain.com username@email.com` - After this you will be prompted to enter your secret in a multi-line prompt. Press **Alt-Return** to save.

If you want loz to generate secret for you, just use `loz make mydomain.com username@email.com` instead. It will generate and save new secret and print it out for you.

### Read secret

`loz get mydomain.com username@email.com` - After this you will be prompted for the master password. Note that you can autocomplete name of domains and usernames by pressing **Tab**.

`loz show mydomain.com` will print all secrets for all usernames under selected domain.

### List entries

`loz ls` will list domains and `loz ls mydomain.com` will list usernames under selected domain.

`loz find searchword` will list all domains and/or usernames that contain a word `searchword`.

### Delete an entry

`loz rm mydomain.com username@email.com` will delete selected username. If that's the only username under selected domain, the whole domain will be removed. If you want to delete a domain with all usernames under it, just type `loz rm mydomain.com`.

### Export/Import

`loz export > backup.csv` will export all secrets in a plain text csv file. You can import backed up file with `loz import backup.csv`. It will ask you if you want to overwrite existing entries.

### Change password

`loz passwd` will prompt you for old and new password. It will then generate new keys and re-encrypt all secrets.

Lozfile and encryption
-------------------------

Lozfile is the json storage of all secrets. It contains plaintext RSA public key and Fernet (password) encrypted private key as well. Public key is used in the background when you are entering or generating new secrets. Private key is useless without your master password, but weak password means weak encryption.

All secrets are encrypted with a very secure RSA 4096. This is slow for encryption and decryption, but allows the asymmetric appraoch and doesn't have a big performance impact on short secrets.

### Compatibility
Backwards compatibility will be guaranteed for all lozfiles created with loz versions 0.1.0 and above. If there is a change in lozfile format, you may be prompted to update your lozfile.

### WARNING
Lozfile is revealing domains and usernames. This is by design to enable autocomplete. Future versions of loz may offer full encryption option, but for not it's not available and it's not a focus. If you are concerned about privacy of your usernames, then loz is not for you!

