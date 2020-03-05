# Network Borg Blog - Resistance is futile

## Requirements
python3 -m pip install -r requirements.txt

## Usage
python3 *****_network_borg.py -y {YAML_GROUP/HOST}

## Change History

### Version 0.1
- Fixed code logic in 'PUSH' operation.
- Improved logging

### Version 0.1.1
- Fixed logic in 'network_borg_genyml.py' which would return a dictionary with 'Host: DEV SWITCH-01' whereas we just require a list of hosts when a YAML Group argument is sent.
- Improved Logging
- Added debug -d option to CLI argument so we don't need to comment/ uncomment
  print lines
- Added network_borg_v50* to do the actual config PUSH

### Version 0.1.2
- Continued fixing CLI argument parsing as initially fixed by Guy

### Version 0.1.3
- Improved Credential Handling in network_borg_v601.py

### Version 0.1.4
- Added Credentials Override CLI Argument
- Improved YAML Handling in network_borg_v602.py
  - All NORNIR handling is now within _network_borg_genyml_v602.py. Stripped NORNIR from network_borg_v602.py
  - _network_borg_genyml_v602.py now returns a yaml_dict {} which uses hostname as the key value and discovered YAML facts as objects.
  - Added Environment field to hosts.yaml (e.g. Production, Development, etc). Not yet used but will be used to improve model forking (i.e. not scrap hostname in _network_borg_dicvry for the word DEV!)
- Back-ported Credentials Handling functionality to network_borg_v000.py.

### Version 0.1.5
- Back-ported YAML Dictionary method as opposed to List so all All NORNIR handling is now within _network_borg_genyml.py.
- Rewrote network_borg_v00*.py files to align with article.
- Rewrote _network_borg_discvry.py module so there is no scraping of hostname for word DEV. Environment is now defined as a variable in the hosts.yaml.
- Added network_borg_v103.py so it now finishes on forking based on model. Forking logic is to be reviewed.
- Scripts tested up to network_borg_v103.py ONLY!!!

### Version 0.1.6
- Both _network_borg_genyml.py and _network_borg_discvry.py now return a Dictionary {} with the FQDN as the key value.
- Tightened up code for network_borg_v10*.py
- Scripts tested up to network_borg_v103.py ONLY!!!

### Version 0.1.7
- Introduced the SESSION_TK (Token) dictionary to simplify the process of passing session variables (e.g. CLI Arguments, Environmental Variables, GetPass) to other modules. Introduced in network_borg_v001.py and propagated up-to network_borg_v103.py

### Version 0.1.8
- Added _network_borg_getset.py to generate a template_set for Jinja2 rendering.
- Added _network_borg_v301.py to demonstrate Jinja2 rendering.
- Improved Logging

### Version 0.1.9
- Introduced the YAML_TK (Token). Putting YAML vars in SESSION_TK didn't make sense.
- Bug Fixes

### Version 0.2
- Structural renaming

### Version 0.2.1
- Expanded to Chapter 3 - GET.

### Version 0.3
- Expanded to Chapter 4 - COMPARE and Chapter 5 - PUSH.
- Improved _network_borg_diffgen.py Logging and Logic.
- Improved network_borg Logging.
- Added netmko and napalm fields to hosts.yaml and updated network_borg accordingly.
- Removed testYAML.py.
- Improved except Exception handling to print out exception message.

### Version 0.3.1
- Added __c501_network_borg.py with improved except Exception handling to print out exception message.

### Version 0.4
- Added NAPALM get_config Getter to get the running-config during Discovery (_network_borg_discvry.py).
- Added _network_borg_dobak.py to run upload config captured during Discovery to FTP. Work in Progress!
- Reduced Logging verbosity throughout.
- Improved _network_borg_diffgen.py Logging.

### Version 0.5
- Offloaded ARGS process in network_bory.py main() to new module, _network_borg_args.py
- Offloaded SYNC process in network_bory.py main() to new module, _network_borg_sync.py
- Improved Password Obfuscation in _network_borg_args.py

### Version 0.5.1
- Improved _network_borg_genyml.py error handling/ logging.
- Dabbled with font formatting to improve readability.

### Version 0.6
- Back-ported _network_borg_args.py to __c002_network_borg.py.
- Back-ported _network_borg_sync.py to __c102_network_borg.py.
- Simplified hosts.yaml by having one driver (NAPALM). In _network_borg_netmko.py we use the NAPALM driver value to set the NetMiko driver value.
- The __c***_network_borg.py and __c***_network_borg_sync.py files now follow the chapter structure from __c103_network_borg.py onwards.

### Version 0.6.1
- Moved J2 Templates to j2templates folder and updated _network_borg_j2rdr.py accordingly.

### Version 0.6.2
- Improved Exception handling in _network_borg_netmko.py.

### Version 0.6.3
- _network_borg_getset.py now supports Production nodes (N7K, N6K, N5K, C3K, C4KS8, C4KX, C6K).
- Added PROCEED? prompt to _network_borg_args.py when -commit CLI argument is defined. Expects 'y[e/es]' input to proceed.
- Corrected typo in 'template_n5k_dev_snmp.j2'.
- Split into network_borg_v0 (locked) and network_borg_v1 (maintained).

### Version 0.7
- Updated _network_borg_args.pw and _network_borg_getset.py and handle Enable Password. Required to update local usernames.
- Added additional logic handling to _network_borg_sync.py so script will only proceed to next step if previous step was successful.
- Updated _network_borg_j2rdr.py to now dynamically render file with a DICT {}. File no longer needs to be touched to handle additional items.

### Version 0.7.1
- Aligned with Blog's new chapter structure.
- Updated _network_borg_sync.py (and back-ported through _cXXX files) so _network_borg_getset.py is logically in a GETSET section as opposed to JINJA2 section.
- Updated _network_borg_discvry.py as host_facts['os_version'] was returned twice. Now returns vendor. Not used in code but may prove useful.

### Version 0.8
- Moved modules to module folder

### Version 0.9
- Moved NXAPI payload definition for NXAPI from _network_borg_sync.py to _network_borg_nxapi.py.
- Wrote _network_borg_nxapi.py so JSON payload structure is no longer defined in GETSET module. GETSET only returns command to be sent and not the entire JSON payload.
- Updated _network_borg_getset.py so only returns Payload command and not entire JSON payload.

### Version 0.9.1
- Logging corrections

### Version 0.9.2
- Merged _network_borg_nxapi_garbx.py into _network_borg_nxapi.py.
- Removed confusing print line from network_borg.py.
- Corrected _network_borg_getset.py incorrectly referencing "elif SESSION_TK['ENV'] == 'Production':" Should be "elif YAML_TK['YAML_env'] == 'Production'".
- Corrected logic in _network_borg_sync.py to break if status returned by _network_borg_nxapi.py or _network_borg_netmko.py is False.
- Corrected missing logging in _network_borg_netmko.py
- Address workflow through _network_borg_sync.py module. Now calls individual functions in a structured manner and only proceeds if status of previous workflow function is True (OK)

### Version 0.9.3
- Updated _network_borg_sync.py conditional workflow login to now be within a while loop.
- Updated _network_borg_diffgen.py to align with new variable names.

### Version 0.9.4
- Added requirements.txt

### Version 0.9.5
- Added colour to debug output
- Hardened logging. Scrip developed on macOS but when running on Linux, dicts were not getting Zeroised but cached leading to confusing output.  

### Version 0.9.6
- Added function to output master_log to file.
- Corrected error in _network_borg_sync sync_getcfg function.
- Updated _network_borg_getset.py to support Production C3K.
- Updated _network_borg_getset.py to reflect new template file naming convention.

### Version 0.9.7
- Aligned chapter modules with Blog.

### Version 0.9.7.1
- Fixed typo in _network_borg_sync.py PUSH function.

### Version 0.9.7.2
- Modified NetMiko connection handler in _network_borg_netmko.py to support fast_cli. Disabled but can be toggled on/ off.

### Version 0.9.8
- Updated copyright and author notice across all files.

### Version 0.9.9
- Linter identified too many blatant errors. Corrected to Maintenance release and back-ported to Blog release.

### Version 0.9.9.1
- Renamed files to align with Blog structure. Appendices files now start __x.
- Merged _network_borg_nxapi_garbx.py module as function into _network_borg_nxapi.py module.
- Changed structure of data sent from _network_borg_sync.py:getcfg to _network_borg_nxapi.py so 'CMD' is no longer extracted within _network_borg_nxapi.py but sent pre-extracted from _network_borg_sync.py:getcfg().

### Version 0.9.9.2
- Corrected logical error in _network_borg_genyml.py which incorrectly generates an error log.
- Renamed __c330 files to __c300.
- Renames __c220 files to __c200.

### Version 0.9.9.3
- Changed __c600_network_borg.py log file name to YYYY_MM_DD_HH_MM_SS as opposed to generic / & : delimiters which are special characters on some systems.

### Version 0.9.9.4
- Drastically improved performance of NetMiko by sending a command set list [] as opposed to individual commands.

### Version 0.9.9.5
- Re-ordered _network_borg_sync.py so GETCFG (network_borg_netmko/nxapi.py) 'get' mode happens before J2 Render (network_borg_j2rdr.py). Preempting future requires to GET more variables to be used in J2RDR.  
- Re-write of _network_borg_j2rdr.py to call the J2 Render using the Python ** keyword arguments. Means we can send as key value pairs as opposed to messily re-naming VARS to VAR0, 1, 2 etc. J2 Template now has the key reference variable.
- Re-write of _network_borg_j2rdr.py to strictly enforce rendering with variables. If J2 Render attempts to render a file with a missing VAR, bomb out and generate error.
- Added NCCLIENT to GETCFG.

### Version 0.9.9.6
- Stripped libraries not used in _network_borg_ncclient.py.
- Added additional logic to _network_borg_ncclient.py and _network_borg_netmko.py to handle drivers which are not supported. 
