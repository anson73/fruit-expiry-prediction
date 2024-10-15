import * as React from "react";
import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TablePagination from "@mui/material/TablePagination";
import TableRow from "@mui/material/TableRow";
import TableSortLabel from "@mui/material/TableSortLabel";
import Paper from "@mui/material/Paper";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
import Switch from "@mui/material/Switch";
import { visuallyHidden } from "@mui/utils";
import Button from "@mui/material/Button";

import Modal from "@mui/material/Modal";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";

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

function EnhancedTableHead(props) {
  const { order, orderBy, onRequestSort } = props;
  const createSortHandler = (property) => (event) => {
    onRequestSort(event, property);
  };

  const headCells = [
    {
      id: "seq",
      label: "No.",
    },
    {
      id: "fruitType",
      label: "Fruit Type",
    },
    {
      id: "uploadTime",
      label: "Upload Time",
    },
    {
      id: "humidity",
      label: "Humidity",
    },
    {
      id: "temperature",
      label: "Temperature",
    },
    {
      id: "purchaseDate",
      label: "Purchase Date",
    },
    {
      id: "expiryDate",
      label: "Expiry Date",
    },
    {
      id: "daysNotify",
      label: "Notification (Days)",
    },
    {
      id: "ConsumeDate",
      label: "ConsumeDate",
    },
    {
      id: "action",
      label: "Action",
    },
  ];

  return (
    <TableHead>
      <TableRow>
        {headCells.map((headCell) => (
          <TableCell
            key={headCell.id}
            align="center"
            padding="normal"
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

export default function EnhancedTable(props) {
  const [order, setOrder] = React.useState("asc");
  const [orderBy, setOrderBy] = React.useState("calories");
  const [page, setPage] = React.useState(0);
  const [dense, setDense] = React.useState(false);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);
  const [rows, setRows] = React.useState(props.historyData);
  const [originalRows, setOriginalRows] = React.useState(props.historyData);
  const [hideConsumed, setHideConsumed] = React.useState(false);

  const [modalOpen, setModalOpen] = React.useState(false);
  const [alertOpen, setAlertOpen] = React.useState(true);
  const [showAlert, setShowAlert] = React.useState(false);

  const handleRequestSort = (event, property) => {
    const isAsc = orderBy === property && order === "asc";
    setOrder(isAsc ? "desc" : "asc");
    setOrderBy(property);
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

  // Consume Product: Set the product to consumed in the db
  // Input: User Id, prediction/product Id, quantity of return value, if consumed products are hidden
  // Return: the specified quantity of the products sorted by
  const consumeProduct = (seq) => {
    let modifiedRows = [];
    let originalRows = [];
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
      originalRows.push(row);
    });
    setRows(modifiedRows);
    setOriginalRows(originalRows);
  };

  const deleteProduct = (seq) => {
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

  const handleModalOpen = () => setModalOpen(true);
  const handleModalClose = () => setModalOpen(false);
  const handleAlertOpen = () => setShowAlert(true);
  const handleAlertClose = () => setShowAlert(false);

  return (
    <Box sx={{ width: "90%" }}>
      <Modal open={showAlert}>
        <Box
          sx={{
            position: "relative",
            display: "flex",
            flexDirection: "column",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: "60%",
            height: "27.5%",
            bgcolor: "background.paper",
            padding: "2rem",
            gap: "1rem",
            alignItems: "center",
          }}
        >
          <h2>Notification</h2>
          <Typography
            style={{
              width: "90%",
            }}
          >
            The following fresh products will expire shortly.
          </Typography>

          <Button
            variant="outlined"
            style={{
              width: "90%",
            }}
            onClick={handleAlertClose}
          >
            Close
          </Button>
        </Box>
      </Modal>
      <Modal open={modalOpen}>
        <Box
          sx={{
            position: "relative",
            display: "flex",
            flexDirection: "column",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: "30%",
            height: "27.5%",
            bgcolor: "background.paper",
            padding: "2rem",
            gap: "1rem",
            alignItems: "center",
          }}
        >
          <h2>Notification Days</h2>
          <Typography
            style={{
              width: "90%",
            }}
          >
            Please input the number of days you would like to be notified prior
            to the expiry date of the product.
          </Typography>
          <TextField
            label="Number of Days"
            type="number"
            variant="filled"
            slotProps={{
              inputLabel: {
                shrink: true,
              },
            }}
            style={{
              width: "90%",
            }}
          />
          <Button
            variant="outlined"
            style={{
              width: "90%",
            }}
          >
            Open modal
          </Button>
          <Button
            variant="outlined"
            style={{
              width: "90%",
            }}
            onClick={handleModalClose}
          >
            Cancel
          </Button>
        </Box>
      </Modal>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
        }}
      >
        <FormControlLabel
          style={{
            padding: "0.5rem",
            marginLeft: "0rem",
            background: "#f2f2f2",
            width: "15rem",
          }}
          control={<Checkbox />}
          label="Hide Consumed Products"
          onChange={(event) => handleHideConsumed()}
        />
        <div
          style={{
            //border: "solid, 1px black",
            width: "calc(100% - 15rem - 10rem)",
          }}
        ></div>
        {alertOpen ? (
          <Button
            //variant="outlined"
            onClick={handleAlertOpen}
            style={{
              height: "3.5rem",
              width: "10rem",
              backgroundColor: "#fc9b9d",
              color: "black",
            }}
          >
            Open Alert
          </Button>
        ) : null}
      </div>

      <Paper sx={{ width: "100%", marginTop: "1rem" }}>
        <TableContainer>
          <Table
            sx={{ minWidth: 750 }}
            aria-labelledby="tableTitle"
            size={dense ? "small" : "medium"}
          >
            <EnhancedTableHead
              order={order}
              orderBy={orderBy}
              onRequestSort={handleRequestSort}
              rowCount={rows.length}
            />
            <TableBody>
              {visibleRows.map((row) => {
                return (
                  <TableRow
                    hover
                    //role="checkbox"
                    tabIndex={-1}
                    key={row.seq}
                  >
                    <TableCell align="left">{row.seq}</TableCell>
                    <TableCell align="left">{row.fruitType}</TableCell>
                    <TableCell align="center">{row.uploadTime}</TableCell>
                    <TableCell align="center">{row.humidity}</TableCell>
                    <TableCell align="center">{row.temperature}</TableCell>
                    <TableCell align="center">{row.purchaseDate}</TableCell>
                    <TableCell align="center">{row.expiryDate}</TableCell>
                    <TableCell align="center">{row.daysNotify}</TableCell>
                    <TableCell align="left">{row.consumeDate}</TableCell>
                    <TableCell align="left">
                      <Button
                        variant="outlined"
                        onClick={() => viewDetails(row.seq)}
                      >
                        View
                      </Button>
                      <notificationModal />
                      <Button
                        variant="outlined"
                        onClick={() => consumeProduct(row.seq)}
                      >
                        {row.consumed ? <>Un-consume</> : <>Consume</>}
                      </Button>
                      <Button variant="outlined" onClick={handleModalOpen}>
                        Open modal
                      </Button>
                      <Button
                        variant="outlined"
                        onClick={() => deleteProduct(row.seq)}
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
