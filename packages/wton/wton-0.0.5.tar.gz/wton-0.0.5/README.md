# Installation

## To use wton package *(comming soon)*

One can install wton by "pip" (a package manager) by simply running the following commands:
```shell
mkdir ~/tonworkdir & cd ~/tonworkdir
python -m venv venv
source venv/bin/activate
pip install wton
wton init
wton --help
```

> WARNING: One can ignore installation of a virtual environment but we highly recommend to use it not to affect the global python packages.

## To contribute

Simply clone this repository and see "Development" section bellow. 

# Usage

## wton-interactive

To start interactive session. **Hasn't been implemented yet.**


---
## wton-gui

To start interactive session. **Hasn't been implemented yet.**


---
## wton

### Basic commands

**Initialize environment**
```shell
$ wton init
```
It sets the required files structure in a current directory:
```
.wton
├── config.yaml
├── whitelist.json
├── keystores
│   ├── *.keystore
├── tonlibjson
│   ├── keystore
│   │   ├── *.blkstate
│   ├── mainnet.json
│   ├── testnet.json
│   ├── configs_info.yaml
```

tonlibjson directory is used when a person uses tonlibjson provider. When one uses toncenter setup it is not required.

**Check package version**
```shell
$ wton --version
wton, version 0.0.1
```

**Get help info for ANY command**
```shell
$ wton --help
Usage: wton [OPTIONS] COMMAND [ARGS]...

Options:
  --version      Show the version and exit.
  -c, --config   Use specific config.yaml file.
  -h, --help     Show this message and exit.

Commands:
  config    Controls config parameters.
  whitelist   Operate with whitelist.
  contract  Operate with contracts.
  init      Initialize .wton workdir in a current directory.
  keystore  Operate with keystores
  wallet    Operate with wallets
```


---
### Config

Config is the file 'config.yaml' where one can change required settings of the wton package.

All fields:
| Name  |                     Description                      |
| :--- | :---------------------------------------------- |
| wton.keystore_name | name of the keystore a person wants to use. |
| wton.provider | toncenter/tonlibjson to access TON. |
| wton.workdir | directory where whitelist and keystores are stored |
| provider.toncenter.api_key | a person's api key for toncenter api |
| provider.toncenter.base_url | url to request (in case one deployed their own toncenter) |
| provider.tonlibjson.config_path | tonlibjson config (in case one deployed their own liteservers) |
| provider.tonlibjson.configs_auto_update | wton requests configs updates from official github repo once a day |
| provider.tonlibjson.cdll_path | in case one have compiled own version of a tonlibjson |
| provider.tonlibjson.workdir | directory where tonlibjson keystore and configs are stored |


**List values of current config setup**

```shell
$ wton config --current-setup
wton.workdir=/path/.wton
provider.tonlibjson.workdir=/path/.wton/tonlibjson
...
```

**List all configs and their values**
```shell
$ wton config --list
/home/.config/wton/config.yaml  provider.tonlibjson.workdir=/path/.wton/tonlibjson
/home/.config/wton/config.yaml  wton.workdir=/path/.wton/
/path/to/workdir/.wton/config.yaml  wton.workdir=/path/.wton
...
```

**Get config value**
```shell
$ wton config --local wton.provider
toncenter
```

**Set config value**
```shell
$ wton config --global wton.provider tonlibjson
```

**Unset config value**
```shell
$ wton config --file ~/.config/wton/config.yaml --unset wton.provider
```

**Download latest TON testnet/mainnet configs**
```shell
$ wton config --update-ton-configs
```

**Switch between testnet/mainnet configs for the current provider**
```shell
$ wton config --local --network testnet
```


---
### Whitelist

Whitelist stores addresses with names linked to them so one does not transfer money to an incorrect address.

**Add a whitelist (name, address) to the whitelist.json**
```shell
$ wton whitelist add main EQB3wZaZJTzRKt+9Ny1+AqdNdq9WIUV6goBhxZqad6XH0oBx
```

**Get address of a whitelist**
```shell
$ wton whitelist get main
EQB3wZaZJTzRKt+9Ny1+AqdNdq9WIUV6goBhxZqad6XH0oBx
```

**List all whitelist contacts**
```shell
$ wton whitelist list --versbose
| Name  |                     Address                      |     State     |      Balance       |
| :---: | :----------------------------------------------: | :-----------: | :----------------: |
| bank  | EQAhE3sLxHZpsyZ_HecMuwzvXHKLjYx4kEUehhOy2JmCcHCT |    active     | 
531223394.35714173 |
| main  | EQB3wZaZJTzRKt+9Ny1+AqdNdq9WIUV6goBhxZqad6XH0oBx | uninitialized |         0          |
```

One can redirect the output of this command into .md file to get a nice table.
```shell
$ wton whitelist list --versbose > whitelist.md
``` 
| Name  |                     Address                      |     State     |      Balance       |
| :---: | :----------------------------------------------: | :-----------: | :----------------: |
| bank  | EQAhE3sLxHZpsyZ_HecMuwzvXHKLjYx4kEUehhOy2JmCcHCT |    active     | 531223394.35714173 |
| main  | EQB3wZaZJTzRKt+9Ny1+AqdNdq9WIUV6goBhxZqad6XH0oBx | uninitialized |         0          |


---
### Keystore

Keystore is a file where wton stores all wallets information.

**Create new keystore**
```shell
$ wton keystore new myCompanyName1.keystore --password MY_SECRET_PASSWORD
```

A person can also specify WTON_KEYSTORE_PASSWORD. If one does not want to use it they must not forget to unset it.
```shell
$ export WTON_KEYSTORE_PASSWORD=MY_SECRET_PASSWORD
$ unset WTON_KEYSTORE_PASSWORD
```

Without either --password flag or environment variable one will be forced to enter the password in a hidden way.
```shell
$ wton keystore new myCompanyName1.keystore
Password []:
```

**List of keystores**
```shell
$ wton keystore list
myCompanyName1.keystore
myCompanyName2.keystore
```


---
### Wallet

**Create a wallet locally**

```shell
$ wton wallet create \
    burner \
    --workchain 0 \
    --version v3r2 \
    --comment "Burner - active wallet for daily usage" \
    --save-to-whitelist burner
```

**Get wallet information**
```shell
$ wton wallet list --versbose
|  Name  | Version |  WC   |                     Address                      |     State     | Balance |
| :----: | :-----: | :---: | :----------------------------------------------: | :-----------: | :-----: |
|  main  |  v3r2   |   0   | EQDmT2DmF4TdnocLahvwPTEL0/xxTCusR7DsAEVCfZUQ2iA8 | uninitialized |    0    |
| burner |  v3r2   |   0   | EQDK8GHxZUcIhq52a8S4c-l2Ce1PEPcz4sqi0qeXsGUw49Mt | uninitialized |    0    |
```

One can redirect the output of this command into .md file to get a nice table.
```shell
$ wton wallet list --versbose > wallets.md
``` 
|  Name  | Version |  WC   |                     Address                      |     State     | Balance |
| :----: | :-----: | :---: | :----------------------------------------------: | :-----------: | :-----: |
|  main  |  v3r2   |   0   | EQDmT2DmF4TdnocLahvwPTEL0/xxTCusR7DsAEVCfZUQ2iA8 | uninitialized |    0    |
| burner |  v3r2   |   0   | EQDK8GHxZUcIhq52a8S4c-l2Ce1PEPcz4sqi0qeXsGUw49Mt | uninitialized |    0    |

**Initialize wallet address as a wallet contract**

> WARNING: To initialize a wallet **one must send some TON coins to their wallet's address** through any interface (web wallet, telegram wallet, etc.).
To validate whether balance has been changed one can run "wton wallet list --versbose" or "wton contract --wallet NAME info" and check the balance field.

```shell
$ wton wallet init burner
```

At that moment wallet's 'state' field should be 'active'.

**Transfer TON coins from the wallet to the whitelist contact**

```shell
$ wton wallet transfer main friendName 24.5 --message "Birthday present!" --ignore-errors 0 --pay-gas-separately 0 --destroy-if-zero 1 --transfer-all 1
```

---
### Contract

Contract allows a person to interact with abstract addresses.


**Get information about an address**

One can query contract by whitelist name/wallet name/abstract address

```shell
$ wton contract --whitelist bank info
@type: raw.fullAccountState
balance: 531223393958066941
code: te6cckECKQEAA/cAART/APSkE/S88sgLAQIBIAIDAgFIBAUE2vIgxwCOgzDbPOCDCNcYIPkBAdMH2zwiwAAToVNxePQOb6Hyn9s8VBq6+RDyoAb0BCD5AQHTH1EYuvKq0z9wUwHwCgHCCAGDCryx8mhTFYBA9A5voSCYDqQgwgryZw7f+COqH1NAufJhVCOjU04eIR8gAgLMBgcCASAMDQIBIAgJAgFmCgsAA9GEAiPymAvHoHN9CYbZ5S7Z4BPHohwfIwAtAKkItdJEqCTItdKlwLUAdAT8ArobBKAATwhbpEx4CBukTDgAdAg10rDAJrUAvALyFjPFszJ4HHXI8gBzxb0AMmACASAODwIBIBQVARW77ZbVA0cFUg2zyCgCAUgQEQIBIBITAXOxHXQgwjXGCD5AQHTB4IB1MTtQ9hTIHj0Dm+h8p/XC/9eMfkQ8qCuAfQEIW6TW3Ey4PkBWNs8AaQBgJQA9rtqA6ADoAPoCAXoCEfyAgPyA3XlP+AXkegAA54tkwAAVrhlXQQDVZnah7EACASAWFwIBSBgZAVG3JVtnhiZGakYQCB6BzfQxwk2EWkAAMxph5i4AWuAmHAtv7hwLd3RuECEBhbVZm2eGq+Bv7bHGiiJwCB6PjfSkEcRgWkAAMcNEEAIa5CS64GT2E5kAOeLKhACQCB6IYFImHFImHFImXEA2YlzNiDAhAgEgGhsCA5k4HB0BEawabZ4vgbYJQCEAFa35QQDMlXah7BhAAQ2pNs8FV8FgIQAVrdws4IBqsztQ9iACINs8AvJl+ABQQ3FDE9s87VQhKAAK0//TBzAEoNs8L65TILDyYhKxAqQls1McubAlgQDhqiOgKLyw8mmCAYag+AEFlwIREAI+PjCOjREQH9s8QNd49EMQvQXiVBZbVHPnVhBT3Ns8VHEKVHq8IiMmJAAg7UTQ0x/TB9MH0z/0BPQE0QBIAY4aMNIAAfKj0wfTB1AD1wEg+QEF+QEVuvKkUAPgbCFwVCATAAwByMv/ywcE1ts87VT4D3AlblOJvrGYEG4QLVDHXwePGzBUJANQTds8UFWgRlAQSRA6SwlTuds8UFQWf+L4AAeDJaGOLCaAQPSWb6UglDBTA7neII4WODk5CNIAAZfTBzAW8AcFkTDifwgHBZJsMeKz5jAGKCUmJwBgcI4pA9CDCNcY0wf0BDBTFnj0Dm+h8qXXC/9URUT5EPKmrlIgsVIDvRShI27mbCIyAH5SML6OIF8D+ACTItdKmALTB9QC+wAC6DJwyMoAQBSAQPRDAvAHjhdxyMsAFMsHEssHWM8BWM8WQBOAQPRDAeIBII6KEEUQNEMA2zztVJJfBuIoABzIyx/LB8sHyz/0APQAyc+7oJU=
data: te6cckEBCwEA5wACHQAAAAEFA2JIYo0AAAAA4AECAgHLAwQAE6AxKLsWAAAAACACASAFBgBD0hjXSLxNT0/5NIH9QcOZRdVYe44qotijXq+Z7uktm6lgBAIBIAcIAgEgCQoAQyyRVFPHNrdpK1tMdvOpDmrux6At6Ydsil7uWJwQRyOhgCAAQwd3bNaR++E+iR7W29FUYcCYsblcgir2Bb6NwzHn1FVxACAAQzgX3I3jBXNLDIo60FJk6XZaBKOdvgPdmXOqYSph92bXwCAAQx+MZxR866FwDTUD5UwIIPll9PguUhDpoyJKd2yPP60YQCCZhU9l
last_transaction_id: {'@type': 'internal.transactionId', 'lt': '28158895000005', 'hash': 'n/Od4tUI78l4XBR9hHS6Y+ORYW3bbInugiHlaKNxlk0='}
block_id: {'@type': 'ton.blockIdExt', 'workchain': -1, 'shard': '-9223372036854775808', 'seqno': 20850197, 'root_hash': 'k/+E+fwSizIM/nAJSIQCmRFjlUHEhMSSh+TBxChbpHY=', 'file_hash': 'SDuvK4eGPQzRGuqZU0UPzPi9+G4DWr4sK+3tQ2tp3dg='}
frozen_hash: 
sync_utime: 1653594345
@extra: 1653594364.911616:1:0.28059912601502424
state: active
```

**Get sequential number of an address**

```shell
$ wton contract --wallet burner seqno
132
```


---
# Development

To run the package during development time, create **/PATH/TO/PERSON/venv/bin/wton** file and add the following code:
```python
#!/PATH/TO/PERSON/venv/bin/python
# -*- coding: utf-8 -*-
import re
import sys

sys.path.append("/PATH/TO/PERSON/FOLDER/WITH/wton")

from wton.ui.direct_cli import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
```

Makefile commands:
```shell
make devenv  - Install requirements
make ci      - Run tests
make build   - Build the package
make publish - Publish to the PyPi
```

To install the build
```shell
pip install dist/wton-0.0.1-py3-none-any.whl
```

To build **tonlibjson** check out the scripts (linux/mac) in the directory: ./devtools/build_tonlibjson/*
