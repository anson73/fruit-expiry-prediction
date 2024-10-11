import React, { useState } from 'react'
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
} from '@mui/material'
import CloudUploadIcon from '@mui/icons-material/CloudUpload'
// variable ? parta : partb
const Prediction = () => {
  let results = [
    {
      results: 'Good',
      expire: '12/12/2024',
      possibilty: '80%',
      accurate: 'Yes',
    },
    {
      results: 'Bad',
      expire: '12/12/2024',
      possibilty: '30%',
      accurate: 'Yes',
    },
    {
      results: 'Medium',
      expire: '12/12/2024',
      possibilty: '60%',
      accurate: 'Yes',
    },
  ]

  const [image, setImage] = useState(null)
  const [fruitType, setfruitType] = useState()
  const [location, setlocation] = useState()
  const [Refrigeration, setrefrigeration] = useState()
  const [PurchaseDate, setPurchaseDate] = useState()
  const handleImageUpdate = (event) => {
    const file = event.target.files[0]
    if (file) {
      const url = URL.createObjectURL(file)
      setImage(url)
    }
  }

  const handlePredict = () => {
    console.log(fruitType)
    console.log(location)
    console.log(Refrigeration)
    console.log('Predict')
  }
  return (
    <Box sx={{ padding: 4, margin: 10}}>
      <Typography variant="h3" align="center" gutterBottom>
        Predication
      </Typography>

      <Grid container spacing={2} justifyContent="center">
        <Grid item xs={12} md={6}>
          <Box
            sx={{
              width: '100%',
              height: 600,
              display: 'flex',
              border: '2px dashed red',
              borderRadius: '10px',
              justifyContent: 'center',
              alignItems: 'center',
              overflow: 'hidden',
            }}>
            {image ? (
              <img src={image} alt="You have already submiited the file" />
            ) : (
              <Typography>Please upload the image</Typography>
            )}
          </Box>

          <Button
            variant="contained"
            component="label"
            fullWidth
            startIcon={<CloudUploadIcon />}
            sx={{ marginTop: 1 }}>
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
          <TextField
            fullWidth
            label="Location"
            variant="outlined"
            value={location}
            onChange={(e) => setlocation(e.target.value)}
            sx={{ marginBottom: 2 }}
          />
          <TextField
            fullWidth
            label="Refrigeration"
            variant="outlined"
            value={Refrigeration}
            onChange={(e) => setrefrigeration(e.target.value)}
            sx={{ marginBottom: 2 }}
          />
          <TextField
            fullWidth
            label="PurchaseDate"
            variant="outlined"
            value={PurchaseDate}
            onChange={(e) => setPurchaseDate(e.target.value)}
            sx={{ marginBottom: 2 }}
          />
          <Button
            variant="contained"
            color="secondary"
            fullWidth
            onClick={handlePredict}>
            Predict
          </Button>

          <Box sx={{ marginTop: 8 }}>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Results</TableCell>
                    <TableCell>Expire Date</TableCell>
                    <TableCell>Possibility</TableCell>
                    <TableCell>Accurate</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {results.map((row) => (
                    <TableRow>
                      <TableCell> {row.results} </TableCell>
                      <TableCell> {row.expire} </TableCell>
                      <TableCell> {row.possibilty} </TableCell>
                      <TableCell> {row.accurate} </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
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
  )
}

export default Prediction
