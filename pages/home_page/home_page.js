Page({
  logo1: function (options) {
    wx.navigateTo({
      url: '../ask_risk/ask_risk'
    })
  },

  logo2: function (options) {
    wx.navigateTo({
      url: '../index/index'
    })
  },

  logo3: function (options) {
    wx.navigateTo({
      // url: ''去网页 
    })
  },

  logo4: function (options) {
    wx.navigateTo({
      url: '../about-us/about-us'
    })
  },


  data: {
    imgUrls: [
      'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1564810751126&di=77cc37e91935e703a8d8402c6fdc409a&imgtype=0&src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fimages%2F20180823%2Fc70f3429fd844aceab5f85011e8f3f01.jpeg',
      'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1564811578927&di=d44eb5a8bbef7a949ebb04473a4bcec1&imgtype=0&src=http%3A%2F%2Fimg.liansuo.com%2Fhtml%2Fimages%2F20180904%2F67571536039367.jpg',
      'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1564811441377&di=b8e472dc4c02b0f4bb45951f0b5b4270&imgtype=0&src=http%3A%2F%2Fwww.btc126.com%2Fuploads%2Fallimg%2F171020%2F0K3333195-0.jpg'
    ],
    indicatorDots: true,
    autoplay: true,
    interval: 5000,
    duration: 1000
  },
  
})