import React from "react";
import { useNavigate } from "react-router-dom";

import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import InputAdornment from "@mui/material/InputAdornment";
import FormControl from "@mui/material/FormControl";
import TextField from "@mui/material/TextField";
import Visibility from "@mui/icons-material/Visibility";
import VisibilityOff from "@mui/icons-material/VisibilityOff";
import Button from "@mui/material/Button";

export default function Login(props) {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = React.useState(false);
  const handleClickShowPassword = () => setShowPassword((show) => !show);
  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  React.useEffect(() => {
    if (props.token) {
      navigate("/history");
    }
  }, [props.token]);

  const login = async () => {
    //const response = await fetch("http://localhost:5005/user/auth/login", {
    //  method: "POST",
    //  body: JSON.stringify({
    //    email,
    //    password,
    //  }),
    //  headers: {
    //    "Content-type": "application/json",
    //  },
    //});
    //const data = await response.json();
    //if (data.error) {
    //  alert(data.error);
    //} else if (data.token) {
    //  console.log(data);
    //  localStorage.setItem("token", data.token);
    //  localStorage.setItem("email", email);
    //  props.setToken(data.token);
    //  navigate("/hostings");
    //}
    props.setToken("000000");
    localStorage.setItem("token", "0000000");
    navigate("/history");
  };

  const Cancel = () => {
    navigate("/landpage");
  };

  return (
    <div
      className="registerPage"
      style={{
        // border: '1px solid red',
        display: "flex",
        height: "80vh",
        justifyContent: "center",
        alignItems: "center",
        overflow: "auto",
      }}
    >
      <Box
        component="form"
        sx={{
          "& > :not(style)": {
            m: 1,
            width: "90%",
            maxWidth: "30rem",
          },
        }}
        noValidate
        autoComplete="off"
        style={{
          padding: "1rem",
          width: "80%",
          maxWidth: "30rem",
          display: "flex",
          alignItems: "center",
          flexDirection: "column",
          backgroundColor: "#ffffff",
        }}
      >
        <h2>Login</h2>
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
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={handleClickShowPassword}
                  onMouseDown={handleMouseDownPassword}
                  edge="end"
                >
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
        <Button variant="outlined" id="login" onClick={login}>
          Submit
        </Button>
        <Button variant="outlined" onClick={Cancel} id="cancelButton">
          Cancel
        </Button>
      </Box>
    </div>
  );
}