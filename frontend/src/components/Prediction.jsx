import React, { useState, useEffect } from "react";
import { Box, Grid, Button, Typography, TextField } from "@mui/material";
import dayjs from "dayjs";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import { DesktopDatePicker } from "@mui/x-date-pickers/DesktopDatePicker";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
// variable ? parta : partb
const Prediction = () => {
  const [image, setImage] = React.useState(null);
  const [imagepreview, setimagepreview] = React.useState(null);
  const [fruitType, setfruitType] = React.useState("");
  const [Refrigeration, setRefrigeration] = React.useState(false);
  const [PurchaseDate, setPurchaseDate] = useState(null);
  const [disableSubmit, setDisableSubmit] = useState(false);
  const [latitude, setlatitude] = React.useState("");
  const [longitude, setlongitude] = React.useState("");
  const [prediction, setPrediction] = React.useState([]);
  const [imageName, setimageName] = React.useState(null);
  const handleImageUpdate = (event) => {
    const file = event.target.files[0];
    if (file) {
      const fileName = file.name;
      const url = URL.createObjectURL(file);
      setimagepreview(url);
      setImage(file);
      setimageName(fileName);
    }
  };

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((postion) => {
      setlatitude(postion.coords.latitude);
      setlongitude(postion.coords.longitude);
    });
  });

  const token = localStorage.getItem("token");
  const handlePredict = async () => {
    const data = new FormData();
    data.append("file", image);
    data.append("fruittype", fruitType);
    data.append("latitude", latitude);
    data.append("longitude", longitude);
    data.append("refrigerated", Refrigeration);
    data.append("purchaseDate", PurchaseDate);

    const response = await fetch(`http://localhost:5005/prediction`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
      body: data,
    });
    const res = await response.text();
    setPrediction(res);
  };
  return (
    <Box sx={{ padding: 4, margin: 10 }}>
      <Typography variant="h3" align="center" gutterBottom>
        Prediction
      </Typography>

      <Grid container spacing={2} justifyContent="center">
        <Grid item xs={12} md={6}>
          <Box
            sx={{
              width: "100%",
              height: 550,
              display: "flex",
              border: "2px dashed red",
              borderRadius: "10px",
              justifyContent: "center",
              alignItems: "center",
              overflow: "hidden",
            }}
          >
            {image ? (
              <img
                src={imagepreview}
                alt={imageName}
                id="product-image"
                style={{ width: "100%", height: 550 }}
              />
            ) : (
              <Typography>Please upload the image</Typography>
            )}
          </Box>

          <Button
            variant="contained"
            component="label"
            fullWidth
            id="imageUpload"
            startIcon={<CloudUploadIcon />}
            sx={{ marginTop: 1 }}
          >
            Upload
            <input type="file" hidden onChange={handleImageUpdate} />
          </Button>
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField
            fullWidth
            label="Product Label"
            variant="outlined"
            id="fruitType"
            value={fruitType}
            onChange={(e) => setfruitType(e.target.value)}
            sx={{ marginBottom: 2 }}
          />
          <FormControl
            id="refridgerationForm"
            fullWidth
            style={{ marginBottom: "0.8rem" }}
          >
            <InputLabel id="demo-simple-select-label">Refrigeration</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="Refrigeration"
              value={Refrigeration}
              label="Refrigeration"
              onChange={(e) => setRefrigeration(e.target.value)}
            >
              <MenuItem value={true}>True</MenuItem>
              <MenuItem value={false}>False</MenuItem>
            </Select>
          </FormControl>
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <DesktopDatePicker
              label="Purchase Date"
              id="purchaseDate"
              onChange={(newValue) => {
                const currentDate = dayjs();
                const dayDifference = currentDate.diff(newValue, "ms");
                setPurchaseDate(newValue.format("YYYY-MM-DD"));
                dayDifference < 0
                  ? setDisableSubmit(true)
                  : setDisableSubmit(false);
              }}
              slotProps={{
                textField: { fullWidth: true },
              }}
            />
          </LocalizationProvider>
          {disableSubmit ? (
            <Typography
              style={{
                width: "90%",
                color: "red",
                margin: "1rem 0rem",
              }}
            >
              Please Input a valid consumption date that is not in the future!
            </Typography>
          ) : (
            <></>
          )}
          <Button
            variant="outlined"
            color="secondary"
            fullWidth
            id="predictButton"
            disabled={disableSubmit}
            onClick={handlePredict}
            style={{ marginTop: "0.8rem", marginBottom: "1rem" }}
          >
            Predict
          </Button>
          <Typography id="prediction-result">
            Estimated Expiry: {prediction}
          </Typography>

          <Box sx={{ marginTop: 8 }}></Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Prediction;
