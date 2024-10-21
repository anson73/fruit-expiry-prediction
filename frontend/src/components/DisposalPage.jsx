import * as React from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import dayjs from "dayjs";
import Modal from "@mui/material/Modal";
import Typography from "@mui/material/Typography";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DesktopDatePicker } from "@mui/x-date-pickers/DesktopDatePicker";

export default function DisposalPage(props) {
  const [days, setDays] = React.useState(0);
  const [disableSubmit, setDisableSubmit] = React.useState(false);

  return (
    <Modal open={props.disposeOpen}>
      <Box
        sx={{
          position: "relative",
          display: "flex",
          flexDirection: "column",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          width: "30%",
          bgcolor: "background.paper",
          padding: "2rem",
          gap: "1rem",
          alignItems: "center",
        }}
      >
        <h2>Dispose this product</h2>
        <Typography
          style={{
            width: "90%",
          }}
        >
          Please input the date that you have disposed this product.
        </Typography>
        <Typography
          style={{
            width: "90%",
          }}
        >
          Fruit Type: {props.row.fruitType}
          <br />
          Image Id: {props.row.imageId}
          <br />
          Purchase Date: {props.row.purchaseDate}
        </Typography>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DesktopDatePicker
            label="Disposal Date"
            onChange={(newValue) => {
              const currentDate = dayjs();
              const dayDifference = currentDate.diff(newValue, "ms");
              setDays(currentDate.diff(newValue, "day"));
              dayDifference < 0
                ? setDisableSubmit(true)
                : setDisableSubmit(false);
            }}
          />
        </LocalizationProvider>
        {disableSubmit ? (
          <Typography
            style={{
              width: "90%",
              color: "red",
            }}
          >
            Please Input a valid disposal date that is not in the future!
          </Typography>
        ) : (
          <></>
        )}
        <Button
          variant="outlined"
          disabled={disableSubmit}
          onClick={() => {
            props.disposeProduct(props.row.imageId, days);
            props.disposeClose();
          }}
          style={{
            width: "90%",
          }}
        >
          Submit
        </Button>
        <Button
          variant="outlined"
          onClick={props.disposeClose}
          style={{
            width: "90%",
          }}
        >
          Cancel
        </Button>
      </Box>
    </Modal>
  );
}