Page({
  logo1: function (options) {
    wx.navigateTo({
      url: '../ask_risk/ask_risk'
    })
  },

  data:{
    // 组件所需的参数
    nvabarData: {
      showCapsule: 1, //是否显示左上角图标   1表示显示    0表示不显示
      title: '原地起飞', //导航栏 中间的标题
    }
  }

})