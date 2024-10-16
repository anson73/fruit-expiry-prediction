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

export default function NotifDates(props) {
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
        Please input the number of days you would like to be notified prior to
        the expiry date of the product.
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
  </Modal>;
}
