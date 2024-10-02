import React from "react";
import Typography from "@mui/material/Typography";
import Avatar from "@mui/material/Avatar";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";

const Profile = () => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: "2rem",
      }}
    >
      <Typography
        variant="caption"
        display="block"
        gutterBottom
        sx={{
          textAlign: "center",
        }}
      >
        <h1>THIS IS A PLACEHOLDER FOR THE USER PROFILE PAGE</h1>
      </Typography>
      <Avatar
        alt="Remy Sharp"
        src="/Users/victor-tien/Downloads/IMG_1727.JPG"
        sx={{ width: "10rem", height: "10rem", border: "1px solid red" }}
      />
      <TextField id="email" required label="Email" variant="outlined" />
    </div>
  );
};

export default Profile;
