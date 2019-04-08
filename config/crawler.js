/*
	H1b case crawler
    Author: Hao Sheng <haosheng@stanford.edu>
    Last update: Apr. 8th, 2019
*/
var configs = {
  domains: ["www.checkee.info"],
  scanUrls: [],
  //  scanUrls: ["https://www.checkee.info/personal_detail.php?casenum=1313"],
  contentUrlRegexes: [/https:\/\/www\.checkee\.info\/personal_detail\.php\?casenum=\d*/],
  helperUrlRegexes: [/https:\/\/www\.checkee\.info\/main\.php\?dispdate=\d*-\d*/],
  fields: [
    {
      name: "user_ID",
      selector: "//td[contains(text(),'ID')]",
      required: true
    },
    {
      name: "case_ID",
      selector: "//td[contains(text(), 'Checkee CaseNum: ')]"
    },
    {
      name: "first_name",
      selector: "//td[contains(text(), 'First Name: ')]"
    },
    {
      name: "last_name",
      selector: "//td[contains(text(), 'Last Name: ')]"
    },
    {
      name: "check_start",
      selector: "//td[contains(text(), 'Check Date: ')]"
    },
    {
      name: "education_university",
      selector: "//td[contains(text(), 'University(College): ')]"
    },
    {
      name: "visa_type",
      selector: "//td[contains(text(), 'Visa Type: ')]"
    },
    {
      name: "degree",
      selector: "//td[contains(text(), 'Degree: ')]"
    },
    {
      name: "visa_entry",
      selector: "//td[contains(text(), 'Visa Entry: ')]"
    },
    {
      name: "job_employer",
      selector: "//td[contains(text(), 'Employer: ')]"
    },
    {
      name: "visa_consulate",
      selector: "//td[contains(text(), 'US Consulate: ')]"
    },
    {
      name: "job_title",
      selector: "//td[contains(text(), 'Job Title: ')]"
    },
    {
      name: "education_major",
      selector: "//td[contains(text(), 'Major: ')]"
    },
    {
      name: "visa_stay",
      selector: "//td[contains(text(), 'Years in Usa: ')]"
    },
    {
      name: "check_status",
      selector: "//td[contains(text(), 'Status: ')]"
    },
    {
      name: "check_end",
      selector: "//td[contains(text(), 'Complete Date: ')]"
    },
    {
      name: "notes",
      selector: "//td[@colspan=3]"
    }
  ]
};

function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

configs.initCrawl = function(site) {
  var options = {
    method: "post", // 列表页是post请求
    headers: {
      referer: "https://www.checkee.info"
    },
    data: { // post请求的参数
      page: 1
    }
  };
  for (var year = 2000; year < 2020; year++) {
    for (var month = 1; month < 13; month++) {
      var helperUrl = "https://www.checkee.info/main.php?dispdate=" + year.toString() + "-" + pad(month, 2);
      site.addScanUrl(helperUrl, options);
    }
  }


}

configs.onProcessContentPage = function(page, content, site) {
  return false;
};

configs.afterExtractField = function(fieldName, data, page, site) {
  if (fieldName != "notes") {
    data = data.split(/:\s+/)[1]
  }
  return data;
};

configs.onEachRow = function(row, dataFrame) {
  if (row.data.user_ID == "") {
    return null;
  }
  return row;
}

var crawler = new Crawler(configs);
crawler.start();