<template>
  <div class="home">
    <md-speed-dial class="speeddial md-bottom-right">
      <md-speed-dial-target @click="openDatePicker()" class="md-primary">
        <md-icon class="mdi mdi-calendar" />
      </md-speed-dial-target>
    </md-speed-dial>
    <div class="mono-main">
      <div class="datepicker-container">
        <md-datepicker
          ref="picker"
          class="datepicker"
          v-model="targetDate"
          :md-disabled-dates="disabledDates"
          :md-immediately="true"
        />
      </div>
      <div v-for="(i, k) in filter(monologue)" :key="k" class="logue">
        <div class="meta">
          <span class="date-info">
            <span class="mdi calendar" />
            <a
              :href="'#' + i.date"
              :id="i.date"
              :name="i.date"
              class="date"
            >{{ getDateString(i.date) }}</a>
          </span>
        </div>
        <div class="content" v-for="(a, b) in i.logue" :key="b">
          <span class="status-info" :class="getColorByType(i.type)">
            <span class="status" :class="getIconByType(i.type)">{{ a.title }}</span>
          </span>
          <div class="logue-content">
            <p>{{ a.contents }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
// @ts-ignore
import MdButton from "vue-material/dist/components/MdButton";
// @ts-ignore
import MdDialog from "vue-material/dist/components/MdDialog";
// @ts-ignore
import MdDatepicker from "vue-material/dist/components/MdDatepicker";
// @ts-ignore
import MdContent from "vue-material/dist/components/MdContent";
// @ts-ignore
import MdSpeedDial from "vue-material/dist/components/MdSpeedDial";
// @ts-ignore
import MdIcon from "vue-material/dist/components/MdIcon";

Vue.use(MdButton)
  .use(MdDialog)
  .use(MdDatepicker)
  .use(MdContent)
  .use(MdSpeedDial)
  .use(MdIcon);

interface Logue {
  date: string;
  title: string;
  contents: string;
}

interface StringMatch {
  [key: string]: string;
}

interface Match {
  [key: string]: StringMatch;
}

export default Vue.extend({
  data() {
    return {
      monologue: [
        {
          date: "2020/04/12",
          type: "info",
          logue: [
            {
              time: "15:03",
              title: "服务器自今日开始 XXXX",
              contents:
                "测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容"
            },
            {
              time: "15:04",
              title: "服务器自今日开始 XXXX",
              contents:
                "测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容"
            },
            {
              time: "16:23",
              title: "服务器自今日开始 XXXX",
              contents:
                "测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容"
            },
            {
              time: "17:32",
              title: "服务器自今日开始 XXXX",
              contents:
                "测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容"
            },
            {
              time: "18:32",
              title: "服务器自今日开始 XXXX",
              contents:
                "测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容"
            }
          ]
        },
        {
          date: "2020/04/03",
          type: "info",
          logue: [
            {
              title: "测试 2",
              contents: "测试 3"
            }
          ]
        },
        {
          date: "2020/04/15",
          type: "warning",
          logue: [
            {
              title: "测试 3",
              contents: "测试 2"
            }
          ]
        },
        {
          date: "2020/04/01",
          type: "solved",
          logue: [
            {
              title: "测试 4",
              contents: "测试 31"
            }
          ]
        },
        {
          date: "2020/03/21",
          type: "solved",
          logue: [
            {
              title: "测试 4",
              contents: "测试 31"
            }
          ]
        },
        {
          date: "2020/03/02",
          type: "solved",
          logue: [
            {
              title: "测试 4",
              contents: "测试 31"
            }
          ]
        },
        {
          date: "2020/05/24",
          type: "solved",
          logue: [
            {
              title: "测试 4",
              contents: "测试 31"
            }
          ]
        }
      ],
      datePickDialog: false,
      targetDate: new Date(),
    };
  },
  methods: {
    filter(mono: Array<Logue>): Array<object> {
      let ar = [];
      ar = mono.slice().sort((a, b) => {
        return new Date(b.date).getTime() - new Date(a.date).getTime();
      });
      return ar;
    },
    getIconByType(type: string): string {
      return this.getClassByType(type, "icon");
    },
    getColorByType(type: string): string {
      return this.getClassByType(type, "color");
    },
    getClassByType(type: string, getType: string): string {
      let match: Match = {
        iconMatch: {
          info: "information",
          warning: "alert",
          solved: "check"
        },
        colorMatch: {
          info: "blue",
          warning: "red",
          solved: "green"
        }
      };
      return match[getType + "Match"][type];
    },
    getDateString(datestr: string): string {
      let date = new Date(datestr);
      let monthMatch = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec"
      ];
      let month = monthMatch[date.getMonth()];
      let day = date.getDate();
      let year = date.getFullYear();
      return `${day} ${month}, ${year}`;
    },
    disabledDates(date: Date) {
      let dates = [];
      for (let i = 0; i < this.monologue.length; i++) {
        dates.push(new Date(this.monologue[i].date).getTime());
      }
      return !dates.includes(date.getTime());
    },
    gotoDate() {
      let date = this.targetDate;
      let date_str = this.getDate(new Date(this.targetDate));
      location.hash = date_str;
    },
    getDate(date: Date, delimiter: string = "/"): string {
      let year = date.getFullYear().toString();
      let month: string | number = date.getMonth() + 1;
      month = month <= 9 ? "0" + month.toString() : month.toString();
      let day: string | number = date.getDate();
      day = day <= 9 ? "0" + day.toString() : day.toString();
      return year + delimiter + month + delimiter + day;
    },
    configMaterial() {
      let locale = (this as any).$material.locale;
      locale.dateFormat = "yyyy/MM/dd";
      locale.days = [
        "星期天",
        "星期一",
        "星期二",
        "星期三",
        "星期四",
        "星期五",
        "星期六"
      ];
      locale.shortDays = [
        "周日",
        "周一",
        "周二",
        "周三",
        "周四",
        "周五",
        "周六"
      ];
      locale.shorterDays = ["日", "一", "二", "三", "四", "五", "六"];
    },
    openDatePicker() {
      console.log(this.$refs.picker);
      // @ts-ignore
      this.$refs.picker.$el.children[0].click();
    },
    hotkey(e: KeyboardEvent) {
      if (e.ctrlKey) {
        switch (e.keyCode) {
          case 71:
            e.preventDefault();
            this.openDatePicker();
        }
      }
    }
  },
  watch: {
    targetDate(v) {
      this.gotoDate();
    }
  },
  mounted() {
    this.configMaterial();
    (this.targetDate as Date | string) = this.getDate(new Date());
    window.addEventListener("keydown", this.hotkey);
  }
});
</script>

<style lang="less" scoped>
.badge {
  border-radius: 2px;
  display: inline-block;
  padding-left: 3px;
  padding-right: 3px;
  padding-top: 0;
  padding-bottom: 0;
  margin-left: 16px;
  font-size: 14px;
  font-weight: 300;
  cursor: default;
  &.latest {
    border: 1px solid #4caf50;
    color: #4caf50;
  }
}

.datepicker-container {
  float: right;
}

.logue {
  box-sizing: content-box;
}

.speeddial {
  position: fixed;
  z-index: 100;

  @media screen and (min-width: 1024px) {
    display: none;
  }
}

.datepicker {
  @media screen and (max-width: 1024px) {
    display: none;
  }
}
</style>