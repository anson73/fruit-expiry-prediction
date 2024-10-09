import * as React from "react";
import PropTypes from "prop-types";
import { alpha } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import TableSortLabel from "@mui/material/TableSortLabel";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Paper from "@mui/material/Paper";
import Checkbox from "@mui/material/Checkbox";
import IconButton from "@mui/material/IconButton";
import Tooltip from "@mui/material/Tooltip";
import FormControlLabel from "@mui/material/FormControlLabel";
import Switch from "@mui/material/Switch";
import DeleteIcon from "@mui/icons-material/Delete";
import FilterListIcon from "@mui/icons-material/FilterList";
import { visuallyHidden } from "@mui/utils";
import Button from "@mui/material/Button";

function createData(
  seq,
  imageId,
  fruitType,
  uploadTime,
  humidity,
  temperature,
  purchaseDate,
  expiryDate,
  consumed,
  consumeDate
) {
  return {
    seq,
    imageId,
    fruitType,
    uploadTime,
    humidity,
    temperature,
    purchaseDate,
    expiryDate,
    consumed,
    consumeDate,
  };
}

const defaultRows = [
  createData(
    1,
    0,
    "Apple",
    "2024-09-20",
    67,
    27,
    "2024-09-20",
    "2024-09-30",
    false,
    ""
  ),
  createData(
    2,
    1,
    "Banana",
    "2024-09-20",
    51,
    34,
    "2024-09-20",
    "2024-09-30",
    true,
    "2024-09-25"
  ),
  createData(
    3,
    2,
    "Tomato",
    "2024-09-20",
    24,
    22,
    "2024-09-20",
    "2024-09-30",
    false,
    ""
  ),
  createData(
    4,
    3,
    "Apple",
    "2024-10-20",
    24,
    22,
    "2024-10-20",
    "2024-10-30",
    false,
    ""
  ),
  createData(
    5,
    4,
    "Banana",
    "2024-10-20",
    24,
    22,
    "2024-10-20",
    "2024-10-30",
    false,
    ""
  ),
  createData(
    6,
    5,
    "Pear",
    "2024-10-20",
    24,
    22,
    "2024-10-20",
    "2024-10-30",
    false,
    ""
  ),
  createData(
    7,
    6,
    "Mango",
    "2024-10-20",
    24,
    22,
    "2024-10-20",
    "2024-10-30",
    false,
    ""
  ),
  createData(
    8,
    7,
    "Grapefruit",
    "2024-10-20",
    24,
    22,
    "2024-10-20",
    "2024-10-30",
    false,
    ""
  ),
];

function getDateNow() {
  const today = new Date();
  const month = today.getMonth() + 1;
  const year = today.getFullYear();
  const date = today.getDate();
  return `${year}-${month}-${date}`;
}

function descendingComparator(a, b, orderBy) {
  if (b[orderBy] < a[orderBy]) {
    return -1;
  }
  if (b[orderBy] > a[orderBy]) {
    return 1;
  }
  return 0;
}

function getComparator(order, orderBy) {
  return order === "desc"
    ? (a, b) => descendingComparator(a, b, orderBy)
    : (a, b) => -descendingComparator(a, b, orderBy);
}

const headCells = [
  {
    id: "seq",
    numeric: true,
    disablePadding: true,
    label: "No.",
  },
  {
    id: "imageId",
    numeric: true,
    disablePadding: false,
    label: "Image ID",
  },
  {
    id: "fruitType",
    numeric: false,
    disablePadding: false,
    label: "Fruit Type",
  },
  {
    id: "uploadTime",
    numeric: false,
    disablePadding: false,
    label: "Upload Time",
  },
  {
    id: "humidity",
    numeric: true,
    disablePadding: false,
    label: "Humidity",
  },
  {
    id: "temperature",
    numeric: true,
    disablePadding: false,
    label: "Temperature",
  },
  {
    id: "purchaseDate",
    numeric: true,
    disablePadding: false,
    label: "Purchase Date",
  },
  {
    id: "expiryDate",
    numeric: true,
    disablePadding: false,
    label: "Expiry Date",
  },
  {
    id: "ConsumeDate",
    numeric: true,
    disablePadding: false,
    label: "ConsumeDate",
  },
  {
    id: "action",
    numeric: false,
    disablePadding: false,
    label: "Action",
  },
];

function EnhancedTableHead(props) {
  const {
    onSelectAllClick,
    order,
    orderBy,
    numSelected,
    rowCount,
    onRequestSort,
  } = props;
  const createSortHandler = (property) => (event) => {
    onRequestSort(event, property);
  };

  return (
    <TableHead>
      <TableRow>
        <TableCell padding="checkbox">
          <Checkbox
            color="primary"
            indeterminate={numSelected > 0 && numSelected < rowCount}
            checked={rowCount > 0 && numSelected === rowCount}
            onChange={onSelectAllClick}
            inputProps={{
              "aria-label": "select all desserts",
            }}
          />
        </TableCell>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align={headCell.numeric ? "center" : "left"}
            padding={headCell.disablePadding ? "none" : "normal"}
            sortDirection={orderBy === headCell.id ? order : false}
          >
            <TableSortLabel
              active={orderBy === headCell.id}
              direction={orderBy === headCell.id ? order : "asc"}
              onClick={createSortHandler(headCell.id)}
            >
              {headCell.label}
              {orderBy === headCell.id ? (
                <Box component="span" sx={visuallyHidden}>
                  {order === "desc" ? "sorted descending" : "sorted ascending"}
                </Box>
              ) : null}
            </TableSortLabel>
          </TableCell>
        ))}
      </TableRow>
    </TableHead>
  );
}

EnhancedTableHead.propTypes = {
  numSelected: PropTypes.number.isRequired,
  onRequestSort: PropTypes.func.isRequired,
  onSelectAllClick: PropTypes.func.isRequired,
  order: PropTypes.oneOf(["asc", "desc"]).isRequired,
  orderBy: PropTypes.string.isRequired,
  rowCount: PropTypes.number.isRequired,
};

function EnhancedTableToolbar(props) {
  const { numSelected } = props;
  return (
    <Toolbar
      sx={[
        {
          pl: { sm: 2 },
          pr: { xs: 1, sm: 1 },
        },
        numSelected > 0 && {
          bgcolor: (theme) =>
            alpha(
              theme.palette.primary.main,
              theme.palette.action.activatedOpacity
            ),
        },
      ]}
    >
      {numSelected > 0 ? (
        <Typography
          sx={{ flex: "1 1 100%" }}
          color="inherit"
          variant="subtitle1"
          component="div"
        >
          {numSelected} selected
        </Typography>
      ) : null}
      {numSelected > 0 ? (
        <Tooltip title="Delete">
          <IconButton>
            <DeleteIcon />
          </IconButton>
        </Tooltip>
      ) : (
        <Tooltip title="Filter list">
          <IconButton>
            <FilterListIcon />
          </IconButton>
        </Tooltip>
      )}
    </Toolbar>
  );
}

EnhancedTableToolbar.propTypes = {
  numSelected: PropTypes.number.isRequired,
};

export default function EnhancedTable() {
  const [order, setOrder] = React.useState("asc");
  const [orderBy, setOrderBy] = React.useState("calories");
  const [selected, setSelected] = React.useState([]);
  const [page, setPage] = React.useState(0);
  const [dense, setDense] = React.useState(false);
  const [rowsPerPage, setRowsPerPage] = React.useState(5);
  const [rows, setRows] = React.useState(defaultRows);
  const [originalRows, setOriginalRows] = React.useState(defaultRows);
  const [hideConsumed, setHideConsumed] = React.useState(false);

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleSelectAllClick = (event) => {
    if (event.target.checked) {
      const newSelected = rows.map((n) => n.seq);
      setSelected(newSelected);
      return;
    }
    setSelected([]);
  };

  const handleClick = (event, id) => {
    const selectedIndex = selected.indexOf(id);
    let newSelected = [];

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, id);
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1)
      );
    }
    setSelected(newSelected);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleChangeDense = (event) => {
    setDense(event.target.checked);
  };

  // Avoid a layout jump when reaching the last page with empty rows.
  const emptyRows =
    page > 0 ? Math.max(0, (1 + page) * rowsPerPage - rows.length) : 0;

  const visibleRows = React.useMemo(
    () =>
      [...rows]
        .sort(getComparator(order, orderBy))
        .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage),
    [order, orderBy, page, rowsPerPage, rows]
  );

  const viewDetails = () => {};

  const consumeProduct = (event, seq) => {
    let modifiedRows = [];
    rows.forEach((row) => {
      //console.log(row.seq, seq, row.consumed);
      if (row.seq === seq && row.consumed === true) {
        row.consumed = false;
        row.consumeDate = "";
        modifiedRows.push(row);
        //console.log("unconsume the product");
      } else if (row.seq === seq && row.consumed === false) {
        row.consumed = true;
        row.consumeDate = getDateNow();
        //console.log("consume the product");
      } else {
        modifiedRows.push(row);
      }
    });
    if (!hideConsumed) {
      setRows(rows.filter((row) => row.consumed === false));
      setHideConsumed(true);
    }
    setRows(modifiedRows);
  };

  const deleteProduct = (event, seq) => {
    setRows(rows.filter((row) => row.seq !== seq));
    setOriginalRows(originalRows.filter((row) => row.seq !== seq));
  };

  const handleHideConsumed = () => {
    setOriginalRows(rows);
    if (!hideConsumed) {
      setRows(rows.filter((row) => row.consumed === false));
      setHideConsumed(true);
    } else {
      setRows(originalRows);
      setHideConsumed(false);
    }
  };

  return (
    <Box sx={{ width: "80%" }}>
      <Paper sx={{ width: "100%", mb: 2, justifyContent: "center" }}>
        <FormControlLabel
          style={{
            padding: "1rem",
            marginLeft: "0rem",
            background: "#f2f2f2",
          }}
          control={<Checkbox />}
          label="Hide Consumed Products"
          onChange={(event) => handleHideConsumed()}
        />
        <EnhancedTableToolbar numSelected={selected.length} />

        <TableContainer>
          <Table
            sx={{ minWidth: 750 }}
            aria-labelledby="tableTitle"
            size={dense ? "small" : "medium"}
          >
            <EnhancedTableHead
              numSelected={selected.length}
              order={order}
              orderBy={orderBy}
              onSelectAllClick={handleSelectAllClick}
              onRequestSort={handleRequestSort}
              rowCount={rows.length}
            />
            <TableBody>
              {visibleRows.map((row, index) => {
                const isItemSelected = selected.includes(row.seq);
                const labelId = `enhanced-table-checkbox-${index}`;

                return (
                  <TableRow
                    hover
                    //role="checkbox"
                    aria-checked={isItemSelected}
                    tabIndex={-1}
                    key={row.seq}
                    selected={isItemSelected}
                  >
                    <TableCell padding="checkbox">
                      <Checkbox
                        color="primary"
                        checked={isItemSelected}
                        onClick={(event) => handleClick(event, row.seq)}
                        inputProps={{
                          "aria-labelledby": labelId,
                        }}
                      />
                    </TableCell>
                    <TableCell
                      component="th"
                      id={labelId}
                      scope="row"
                      padding="none"
                      align="left"
                    >
                      {row.seq}
                    </TableCell>
                    <TableCell align="center">{row.imageId}</TableCell>
                    <TableCell align="left">{row.fruitType}</TableCell>
                    <TableCell align="left">{row.uploadTime}</TableCell>
                    <TableCell align="left">{row.humidity}</TableCell>
                    <TableCell align="left">{row.temperature}</TableCell>
                    <TableCell align="left">{row.purchaseDate}</TableCell>
                    <TableCell align="left">{row.expiryDate}</TableCell>
                    <TableCell align="left">{row.consumeDate}</TableCell>
                    <TableCell align="left">
                      <Button
                        variant="outlined"
                        onClick={(event) => viewDetails(event, row.seq)}
                      >
                        View
                      </Button>
                      <Button
                        variant="outlined"
                        onClick={(event) => consumeProduct(event, row.seq)}
                      >
                        {row.consumed ? <>Un-consume</> : <>Consume</>}
                      </Button>
                      <Button
                        variant="outlined"
                        onClick={(event) => deleteProduct(event, row.seq)}
                      >
                        Delete
                      </Button>
                    </TableCell>
                  </TableRow>
                );
              })}
              {emptyRows > 0 && (
                <TableRow
                  style={{
                    height: (dense ? 33 : 53) * emptyRows,
                  }}
                >
                  <TableCell colSpan={6} />
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={rows.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
      <FormControlLabel
        control={<Switch checked={dense} onChange={handleChangeDense} />}
        label="Dense padding"
      />
    </Box>
  );
}
