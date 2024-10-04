
$(()=>{
    $.get("/api/dashboard/stats?command=cat ../assets/stats.json", (res)=>{
      const stats = JSON.parse(res);
      $("#lastUpdate p").text(stats.lastUpdate)
      $(".card-visitors .data").text(stats.connectedUsers);
      $(".card-orders .data").text(stats.newOrders);
      $(".card-traffic .data").text(stats.totalTraffic)
    });
  });
  