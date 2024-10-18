import React from "react";
import Typography from "@mui/material/Typography";

import HistoryTable from "./HistoryTable";

const History = () => {
  const [order, setOrder] = React.useState("asc");
  const [history, setHistory] = React.useState([]);
  const [rowsPerPage, setRowsPerPage] = React.useState(5);
  const [orderBy, setOrderBy] = React.useState("fruitType");
  const [updateData, setUpdateData] = React.useState(false);
  const [hideConsumed, setHideConsumed] = React.useState(false);
  const [alertContent, setAlertContent] = React.useState([]);
  const [totalItem, setTotalItem] = React.useState(0);
  const [page, setPage] = React.useState(0);

  React.useEffect(() => {
    async function getHistoryData() {
      let hideConsumedVariable = "unhide";
      hideConsumed
        ? (hideConsumedVariable = "hide")
        : (hideConsumedVariable = "unhide");
      const response = await fetch(
        `http://localhost:5005/history?filter=${hideConsumedVariable}&page=${
          page + 1
        }&size=${rowsPerPage}&sort=${orderBy}&order=${order}`,
        {
          method: "GET",
          headers: {
            "Content-type": "application/json",
          },
        }
      );
      const data = await response.json();
      setHistory(data[0]);
      setTotalItem(data[1]);
      //console.log(data);
      setUpdateData(false);
    }
    async function getAlertData() {
      const response = await fetch(`http://localhost:5005/history/alert`, {
        method: "GET",
        headers: { "Content-type": "application/json" },
      });
      const data = await response.json();
      setAlertContent(data);
    }
    getHistoryData();
    getAlertData();
  }, [order, orderBy, updateData, hideConsumed, rowsPerPage, page]);

  //console.log(history);
  console.log(alertContent);

  const controlHideConsumed = () => {
    setPage(0);
    hideConsumed ? setHideConsumed(false) : setHideConsumed(true);
  };

  const consumeProduct = async (imageId) => {
    const response = await fetch(
      `http://localhost:5005/history/consume?imageid=${imageId}`,
      {
        method: "POST",
        headers: { "Content-type": "application/json" },
      }
    );
    //console.log(response);
    if (response.status !== 200) {
      console.log("Error! Invalid Consumption!");
    }
    setUpdateData(true);
  };

  const changeNotifDate = async (imageId, days) => {
    const response = await fetch(
      `http://localhost:5005/history/notification?imageid=${imageId}&days=${days}`,
      { method: "POST", headers: { "Content-type": "application/json" } }
    );
    if (response.status !== 200) {
      console.log("Error! Invalid Notification Date Change!");
    }
    setUpdateData(true);
  };

  const deleteProduct = async (imageId) => {
    const response = await fetch(
      `http://localhost:5005/history/delete?imageid=${imageId}`,
      {
        method: "DELETE",
        headers: { "Content-type": "application/json" },
      }
    );
    //console.log(response);
    if (response.status !== 200) {
      console.log("Error! Invalid Delete!");
    }
    setUpdateData(true);
  };

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
        <HistoryTable
          historyData={history}
          order={order}
          orderBy={orderBy}
          setOrder={setOrder}
          setOrderBy={setOrderBy}
          deleteProduct={deleteProduct}
          setUpdateData={setUpdateData}
          consumeProduct={consumeProduct}
          controlHideConsumed={controlHideConsumed}
          changeNotifDate={changeNotifDate}
          rowsPerPage={rowsPerPage}
          setRowsPerPage={setRowsPerPage}
          alertContent={alertContent}
          totalItem={totalItem}
          page={page}
          setPage={setPage}
        />
      </div>
    </div>
  );
};

export default History;
