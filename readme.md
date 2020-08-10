# a simple IO benchmark

- `bench1`: Using `.tofile()`, test the write speed of a numpy array
- `bench2`: Using MPI-IO, test the write speed of a numpy array
- `bench3`: Using `.write()`, test the write speed of a numpy array
- `bench4`: Using `np.memmap()`, test the write speed of a numpy array

## Usage
- modify `nlist`, then
```python
python bench1.py
```
- to plot,
```python
python plot-rate-vs-mb.py bench1.npz
```

## Notes
- https://stackoverflow.com/questions/50561111/numpy-reading-writing-to-file-performance-specifically-ndarray-tofile
- https://stackoverflow.com/questions/30329726/fastest-save-and-load-options-for-a-numpy-array
- https://numpy.org/doc/stable/reference/generated/numpy.memmap.html
- https://github.com/nschloe/perfplot
- https://stackoverflow.com/questions/51391713/efficient-way-of-writing-numpy-arrays-to-file-in-python
