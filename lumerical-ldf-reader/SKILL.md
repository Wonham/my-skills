---
name: lumerical-ldf-reader
description: Use when inspecting, validating, converting, or comparing Ansys Lumerical MODE or FDTD .ldf D-card files on a machine without Lumerical installed.
---

# Lumerical LDF Reader

Use the bundled read-only parser for Lumerical D-card data. It is verified against a Lumerical-generated MATLAB export for `Lumerical data file 1, version 1.0` MODE/FDE mode fields.

## Workflow

1. Run the parser before attempting manual binary inspection:

   ```bash
   python scripts/lumerical_ldf.py input.ldf --json
   ```

2. Inspect the reported version, D-card name, record names, shapes, dtypes, and scalar values.
3. Access arrays from Python with `read_ldf(path).cards[0]["Ex"]`, or export them:

   ```bash
   python scripts/lumerical_ldf.py input.ldf --export output.npz
   python scripts/lumerical_ldf.py input.ldf --export output.mat
   ```

4. For mode-field analysis, retain `Ex/Ey/Ez/Hx/Hy/Hz`, coordinates, frequency, and available mode scalars such as `neff`, `ng`, `loss`, polarization fraction, and effective area.

## Data contract

| Item | Behavior |
|---|---|
| Complex fields | Returned as NumPy `complex128` arrays |
| Array order | Lumerical column-major order is restored; native singleton dimensions are retained |
| `.npz` export | Requires NumPy |
| `.mat` export | Writes MATLAB v5 through SciPy |
| Lumerical installation | Not required |
| Unsupported version/layout | Raises `LDFError` instead of guessing |

Use `numpy.squeeze` for plotting only when singleton axes are understood. Preserve native shapes for archival comparison and round-trip checks.

## Boundaries

- Treat this as an unofficial parser for a proprietary, undocumented binary format.
- Do not remove version, marker, count, or truncation checks to make an unknown file parse.
- If a new file raises `LDFError`, record its header/version and add a regression fixture before extending the parser.
- The tool reads and converts LDF data; it does not write LDF files or recreate a Lumerical D-card.

## Common mistakes

- MATLAB v7.3 files are HDF5: read them with `h5py`, not `scipy.io.loadmat`.
- HDF5 MATLAB storage may reverse displayed axes. Compare coordinates and known samples before transposing fields.
- A newly solved eigenmode may differ by global complex phase. Align phase before declaring two independently solved fields different.
