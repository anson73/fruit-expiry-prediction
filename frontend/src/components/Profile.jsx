import React from "react";
import { useNavigate } from "react-router-dom";

import Typography from "@mui/material/Typography";
import Avatar from "@mui/material/Avatar";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import IconButton from "@mui/material/IconButton";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import InputAdornment from "@mui/material/InputAdornment";
import FormControl from "@mui/material/FormControl";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import Button from "@mui/material/Button";
import CloudUploadIcon from '@mui/icons-material/CloudUpload'

const Profile = () => {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [daysNotify, setDaysNotify] = React.useState(3);
  const [newPassword, setNewPassword] = React.useState("");
  const [newPasswordConfirmed, setNewPasswordConfirmed] = React.useState("");
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = React.useState(false);
  const handleClickShowPassword = () => setShowPassword((show) => !show);
  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };
  const [image, setImage] = React.useState(null)
  const handleImageUpdate = (event) => {
    const file = event.target.files[0]
    if (file) {
      const url = URL.createObjectURL(file)
      setImage(url)
    }
  }

  const Submit = () => {
    navigate("/history");
  };

  const Cancel = () => {
    navigate("/history");
  };

  return (
    <div
      style={{
        //border: "1px solid black",
        padding: "3rem 0rem",
        //width: "80%",
        //maxWidth: "20rem",
        display: "flex",
        alignItems: "center",
        flexDirection: "column",
        backgroundColor: "#ffffff",
      }}
    >
      <Box
        component="form"
        sx={{
          "& > :not(style)": {
            m: 1,
            width: "90%",
            //maxWidth: "20rem",
          },
        }}
        noValidate
        autoComplete="off"
        style={{
          //border: "1px solid red",
          //height: "80%",
          width: "80%",
          maxWidth: "30rem",
          display: "flex",
          alignItems: "center",
          //justifyContent: "center",
          flexDirection: "column",
          backgroundColor: "#ffffff",
        }}
      >
        <Avatar
          alt="Remy Sharp"
          src= {image}
          style={{ width: "15rem", height: "15rem" }}
        />
        <Button
            variant="contained"
            component="label"
            fullWidth
            startIcon={<CloudUploadIcon />}
            sx={{ marginTop: 1 }}>
            Upload Avatar
            <input type="file" hidden onChange={handleImageUpdate} />
          </Button>
          
        <TextField
          id="email"
          required
          label="Email"
          variant="outlined"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <FormControl variant="outlined" required>
          <InputLabel htmlFor="outlined-adornment-password">
            Password
          </InputLabel>
          <OutlinedInput
            id="outlined-adornment-password"
            data-testid="outlined-adornment-password"
            type={showPassword ? "text" : "password"}
            endAdornment={
              <InputAdornment position="end">
                <IconButton aria-label="toggle password visibility" edge="end">
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            }
            label="Password"
            value={password}
            required={true}
            onChange={(e) => setPassword(e.target.value)}
          />
        </FormControl>
        <FormControl variant="outlined" required>
          <InputLabel htmlFor="outlined-adornment-password">
            New Password
          </InputLabel>
          <OutlinedInput
            id="outlined-adornment-password"
            data-testid="outlined-adornment-password"
            type={showPassword ? "text" : "password"}
            endAdornment={
              <InputAdornment position="end">
                <IconButton aria-label="toggle password visibility" edge="end">
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            }
            label="New Password"
            value={newPassword}
            required={true}
            onChange={(e) => setNewPassword(e.target.value)}
          />
        </FormControl>
        <FormControl variant="outlined" required>
          <InputLabel htmlFor="outlined-adornment-password">
            New Password Confirmation
          </InputLabel>
          <OutlinedInput
            id="outlined-adornment-password"
            data-testid="outlined-adornment-password"
            type={showPassword ? "text" : "password"}
            endAdornment={
              <InputAdornment position="end">
                <IconButton aria-label="toggle password visibility" edge="end">
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            }
            label="New Password Confirmation"
            value={newPasswordConfirmed}
            required={true}
            onChange={(e) => setNewPasswordConfirmed(e.target.value)}
          />
        </FormControl>
        <TextField
          id="notificationTime"
          required
          label="Notify Days before Expiry"
          variant="outlined"
        />
        <textarea
          name="postContent"
          defaultValue="Profile Remarks..."
          rows="10"
        />
        <Button variant="outlined" id="submit" onClick={Submit}>
          Submit
        </Button>
        <Button variant="outlined" id="cancel" onClick={Cancel}>
          Cancel
        </Button>
      </Box>
    </div>
  );
};

export default Profile;
