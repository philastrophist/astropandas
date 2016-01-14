from astropy import table
from astropy.table.column import MaskedColumn
from collections import OrderedDict
import numpy as np

class Table(table.Table):
    def to_pandas(self):
        """
        Return a :class:`pandas.DataFrame` instance

        Returns
        -------
        dataframe : :class:`pandas.DataFrame`
            A pandas :class:`pandas.DataFrame` instance

        Raises
        ------
        ImportError
            If pandas is not installed
        ValueError
            If the Table contains mixin or multi-dimensional columns
        """
        from pandas import DataFrame

        if self.has_mixin_columns:
            raise ValueError("Cannot convert a table with mixin columns to a pandas DataFrame")

        if any(getattr(col, 'ndim', 1) > 2 for col in self.columns.values()):
            raise ValueError("Cannot convert a table with multi-dimensional columns to a pandas DataFrame")

        out = OrderedDict()

        for parent_name, parent_column in self.columns.items():
            try:
                ns = range(parent_column.shape[1])
            except IndexError:
                todo = [(parent_name, parent_column)]
            else:
                todo = [('{}({})'.format(parent_name, i), parent_column[:, i]) for i in ns]
            for name, column in todo:
                if name == 'SDSSID_1':
                    print column.dtype
                if isinstance(column, MaskedColumn):
                    if column.dtype.kind in ['i', 'u']:
                        out[name] = column.astype(float).filled(np.nan)
                    elif column.dtype.kind in ['f', 'c']:
                        out[name] = column.filled(np.nan)
                    else:
                        out[name] = column.astype(np.object).filled(np.nan)
                else:
                    out[name] = column

                if out[name].dtype.byteorder not in ('=', '|'):
                    out[name] = out[name].byteswap().newbyteorder()
        return DataFrame(out)

