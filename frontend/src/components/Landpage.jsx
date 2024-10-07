import React, { useState } from "react";
import { Box, Typography } from "@mui/material";

const Landpage = () => {
  return (
    <Box
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",

        height: "80vh",
        overflow: "auto",
      }}
    >
      <Typography variant="h1" align="center">
        Welcome!
      </Typography>
    </Box>
  );
};

export default Landpage;
