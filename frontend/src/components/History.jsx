import React from "react";
import Typography from "@mui/material/Typography";

import HistoryTable from "./HistoryTable";

const History = () => {
  function createData(
    seq,
    imageId,
    fruitType,
    uploadTime,
    humidity,
    temperature,
    purchaseDate,
    expiryDate,
    daysNotify,
    consumed,
    consumeDate
  ) {
    return {
      seq,
      imageId,
      fruitType,
      uploadTime,
      humidity,
      temperature,
      purchaseDate,
      expiryDate,
      daysNotify,
      consumed,
      consumeDate,
    };
  }

  const defaultRows = [
    createData(
      1,
      0,
      "Apple",
      "2024-09-20",
      67,
      27,
      "2024-09-20",
      "2024-09-30",
      5,
      false,
      ""
    ),
    createData(
      2,
      1,
      "Banana",
      "2024-09-20",
      51,
      34,
      "2024-09-20",
      "2024-09-30",
      3,
      true,
      "2024-09-25"
    ),
    createData(
      3,
      2,
      "Tomato",
      "2024-09-20",
      24,
      22,
      "2024-09-20",
      "2024-09-30",
      4,
      false,
      ""
    ),
    createData(
      4,
      3,
      "Apple",
      "2024-10-20",
      24,
      22,
      "2024-10-20",
      "2024-10-30",
      2,
      false,
      ""
    ),
    createData(
      5,
      4,
      "Banana",
      "2024-10-20",
      24,
      22,
      "2024-10-20",
      "2024-10-30",
      6,
      false,
      ""
    ),
    createData(
      6,
      5,
      "Pear",
      "2024-10-20",
      24,
      22,
      "2024-10-20",
      "2024-10-30",
      4,
      false,
      ""
    ),
    createData(
      7,
      6,
      "Mango",
      "2024-10-20",
      24,
      22,
      "2024-10-20",
      "2024-10-30",
      3,
      false,
      ""
    ),
    createData(
      8,
      7,
      "Grapefruit",
      "2024-10-20",
      24,
      22,
      "2024-10-20",
      "2024-10-30",
      2,
      false,
      ""
    ),
  ];

  return (
    <div
      className="historyPage"
      style={{
        paddingTop: "3rem",
        //border: "1px solid red",
        //display: "flex",
        justifyContent: "center",
        alignItems: "center",
        overflow: "",
      }}
    >
      <Typography
        variant="caption"
        display="block"
        gutterBottom
        sx={{
          textAlign: "center",
          //display: "flex",
          //alignItems: "Center",
          //justifyContent: "Center",
        }}
      >
        <h1>Welcome! This is your freshness prediction history!</h1>
      </Typography>
      <div
        style={{
          //border: "10px solid red",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
        }}
      >
        <HistoryTable historyData={defaultRows} />
      </div>
    </div>
  );
};

export default History;
