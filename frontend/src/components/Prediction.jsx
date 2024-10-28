import React, { useState, useEffect } from "react";
import {
  Box,
  Grid,
  Button,
  Typography,
  TextField,
  TableContainer,
  TableCell,
  TableRow,
  TableHead,
  Paper,
  TableBody,
  Table,
  Checkbox,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
// variable ? parta : partb
const Prediction = () => {
  const [image, setImage] = React.useState(null);
  const [imagepreview, setimagepreview] = React.useState(null);
  const [fruitType, setfruitType] = React.useState("");
  const [Refrigeration, setrefrigeration] = React.useState(false);
  const [latitude, setlatitude] = React.useState("");
  const [longitude, setlongitude] = React.useState("");
  const [prediction, setPrediction] = React.useState([]);
  const handleImageUpdate = (event) => {
    const file = event.target.files[0];
    setImage(file);
    if (file) {
      const url = URL.createObjectURL(file);
      setimagepreview(url);
    }
  };

  useEffect(()=>{
    navigator.geolocation.getCurrentPosition((postion)=>{
      setlatitude(postion.coords.latitude)
      setlongitude(postion.coords.longitude)
    })
  })

  const token = localStorage.getItem("token");
  const handlePredict = async () => {
    const data = new FormData();
    data.append("file", image);
    data.append("fruittype", fruitType);
    data.append("latitude", latitude);
    data.append("longitude", longitude);
    data.append("refrigerated", Refrigeration);

    const response = await fetch(
      `http://localhost:5005/prediction`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: data,
      });
      const res = await response.text()
      setPrediction(res)
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
              <img src={imagepreview} alt="Uploaded" />
            ) : (
              <Typography>Please upload the image</Typography>
            )}
          </Box>

          <Button
            variant="contained"
            component="label"
            fullWidth
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
            label="Fruit Type"
            variant="outlined"
            value={fruitType}
            onChange={(e) => setfruitType(e.target.value)}
            sx={{ marginBottom: 2 }}
          />
          <Typography >
            Refrigerated: 
          </Typography>
          <Checkbox
            onChange={() => setrefrigeration(!Refrigeration)}
          >
          </Checkbox>
          <Button
            variant="contained"
            color="secondary"
            fullWidth
            onClick={handlePredict}
          >
            Predict
          </Button>
          <Typography >
            Estimated Expiry: {prediction}
          </Typography>

          <Box sx={{ marginTop: 8 }}>
            
          </Box>
        </Grid>
      </Grid>

      {/* <Box justifyContent="space-around" display="flex" marginTop="4">
        <Button variant="contained" color="primary">
          Prediction
        </Button>

        <Button variant="contained" color="secondary">
          History
        </Button>
      </Box> */}
    </Box>
  );
};

export default Prediction;
