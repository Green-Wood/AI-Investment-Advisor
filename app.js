//app.js
App({
  onLaunch: function () {
    // 展示本地存储能力
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)

    // 登录
    wx.login({
      success: res => {
        // 发送 res.code 到后台换取 openId, sessionKey, unionId
      }
    })

    wx.getSystemInfo({
      success: (res) => {
        this.globalData.height = res.statusBarHeight
      }
    })
    // 获取用户信息
    wx.getSetting({
      success: res => {
        if (res.authSetting['scope.userInfo']) {
          // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
          wx.getUserInfo({
            success: res => {
              // 可以将 res 发送给后台解码出 unionId
              this.globalData.userInfo = res.userInfo

              // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
              // 所以此处加入 callback 以防止这种情况
              if (this.userInfoReadyCallback) {
                this.userInfoReadyCallback(res)
              }
            }
          })
        }
      }
    })
  },
  globalData: {
    userInfo: null,
    height: 0,
    question: [
      { "question": "您的家庭可支配年收入为(折合人民币) ：", "option": { "A": "100万元以下", "B": "100—500万元", "C": "500—1000万元", "D": "1000万元以上" } }, 
      { "question": "在您每年的家庭可支配收入中，可用于金融投资(储蓄存款除外)的比例为：", "option": { "A": "小于10%  ", "B": "10%至25% ", "C": "25%至50%  ", "D": "50%以上" } },
      { "question": "您计划的投资期限是多久：", "option": { "A": "1年以下", "B": "1至3年", "C": "3至5年", "D": "5年以上" } },
      { "question": "您是否有尚未清偿的数额较大的债务，如有，其性质是：", "option": { "A": "有，亲戚朋友借款", "B": "有，信用卡欠款、消费信贷等短期信用债务", "C": "有，住房抵押贷款等长期定额债务", "D": "没有" } },
      { "question": "以下哪项描述最符合您的投资态度：", "option": { "A": "厌恶风险，不希望本金损失，希望获得稳定回报", "B": "保守投资，不希望本金损失，愿意承担一定幅度的收益波动", "C": "寻求资金的较高收益和成长性，愿意为此承担有限本金损失 ", "D": "希望赚取高回报，愿意为此承担较大本金损失" } },
      { "question": "希望赚取高回报，愿意为此承担较大本金损失", "option": { "A": "10%以内", "B": "10%-30%", "C": "30%-50%", "D": "超过50%" } }
      ]
  }
})