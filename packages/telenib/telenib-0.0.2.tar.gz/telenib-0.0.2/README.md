# telenib

Read header of remote nifti according to [nifti1 spec](https://nifti.nimh.nih.gov/pub/dist/src/niftilib/nifti1.h) and [nifti2 spec](https://nifti.nimh.nih.gov/pub/dist/doc/nifti2.h) either gzipped or not.

## Requirements

server must support [RANGE request](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range).

- requests
- nibabel

## Why?

For large nifti files, it is often not feasible to download the full nifti file in order to access the header. 

## Installation

- via pip
```sh
pip install telenib
```

## Usage

```python
from telenib import get_nii_header
from nibabel import Nifti1Header, Nifti2Header

nii_url="https://nifti.nimh.nih.gov/nifti-1/data/avg152T1_RL_nifti.nii.gz"
tele_header = get_nii_header(nii_url)

assert isinstance(tele_header, Nifti1Header) or isinstance(tele_header, Nifti2Header)
```

One could also add any custom header
```python
from telenib import get_nii_header

# from https://nifti.nimh.nih.gov/nifti-1/data
nii_url="https://my.example.co/my/dir/nii.nii.gz"
tele_header = get_nii_header(nii_url, headers={
    'Authorization': f'token my-secret-token'
})

print(tele_header)
```

## License

MIT
