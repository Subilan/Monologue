<template>
  <div class="home">
    <div class="mono-main">
      <md-empty-state v-if="empty">
        <span class="md-empty-state-icon mdi mdi-help-circle-outline" />
        <span class="md-empty-state-label">空页面</span>
        <span class="md-empty-state-description">此页面目前没有任何内容</span>
      </md-empty-state>
      <div v-if="!empty">
        <md-speed-dial class="speeddial md-bottom-right">
          <md-speed-dial-target @click="openDatePicker()" class="md-primary">
            <md-icon class="mdi mdi-calendar" />
          </md-speed-dial-target>
        </md-speed-dial>
        <div class="datepicker-container">
          <md-button class="md-primary md-raised md-icon-button" @click="openDatePicker()">
            <md-icon class="mdi mdi-calendar" />
          </md-button>
          <md-datepicker
            ref="picker"
            class="datepicker"
            v-model="targetDate"
            :md-immediately="true"
          />
        </div>
        <div v-for="(i, k) in monologue" :key="k" class="logue">
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
            <span class="status-info" :class="getColorByType(a.type)">
              <span class="status" :class="getIconByType(a.type)">{{ a.title }}</span>
              <span
                v-if="auth"
                class="edit"
                @click="$router.push({name: 'admin-edit-event', params: {id: a.id}})"
              >编辑</span>
            </span>
            <div class="logue-content" v-html="a.contents"></div>
          </div>
        </div>
      </div>
      <div class="load-more">
        <md-button
          v-if="showLoadNextButton"
          @click="loadNextTen()"
          class="md-primary md-raised load-more-button"
        >加载更多</md-button>
        <md-progress-spinner md-mode="indeterminate" v-if="showLoading" class="loading" />
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
// @ts-ignore
import MdEmptyState from "vue-material/dist/components/MdEmptyState";
// @ts-ignore
import MdProgress from "vue-material/dist/components/MdProgress";

Vue.use(MdButton)
  .use(MdDialog)
  .use(MdDatepicker)
  .use(MdContent)
  .use(MdSpeedDial)
  .use(MdIcon)
  .use(MdEmptyState)
  .use(MdProgress);

export default Vue.extend({
  data() {
    return {
      monologue: [],
      datePickDialog: false,
      targetDate: new Date(),
      empty: false,
      auth: false,
      limitStart: 10,
      showLoadNextButton: false,
      showLoading: false,
      total: 0
    };
  },
  methods: {
    getArray(array: Array<LogueOrigin>): Array<LogueArrayItem> {
      let arr: Array<LogueArrayItem> = [];
      array.forEach((k, i) => {
        let ix = -1;
        let d = k.date.split(" ");
        let date = d[0];
        let time = d[1];
        let sameDay = arr.some((r, j) => {
          if (date === r.date.split(" ")[0]) {
            ix = j;
            return true;
          }
          return false;
        });
        if (!sameDay) {
          arr.push({
            date: date,
            logue: [
              {
                id: k.id,
                title: k.title,
                type: k.type,
                contents: k.contents,
                time: time
              }
            ]
          });
        } else {
          arr[ix].logue.push({
            id: k.id,
            title: k.title,
            type: k.type,
            contents: k.contents,
            time: time
          });
        }
      });
      arr = arr.slice().sort((a, b) => {
        return new Date(b.date).getTime() - new Date(a.date).getTime();
      });
      return arr;
    },
    getIconByType(type: string): string {
      return this.getClassByType(type, "icon");
    },
    getColorByType(type: string): string {
      return this.getClassByType(type, "color");
    },
    getClassByType(type: string, getType: string): string {
      let match: MatchObject = {
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
    /* need fix
    disabledDates(date: Date) {
      let dates: Array<number> = [];
      for (let i = 0; i < this.f_monologue.length; i++) {
        dates.push(new Date((this.f_monologue[i] as LogueArrayItem).date).getTime());
      }
      // @ts-ignore
      return !dates.includes(date.getTime());
    },*/
    gotoDate() {
      let date = this.targetDate;
      let date_str = this.getDate(new Date(this.targetDate));
      location.hash = date_str;
    },
    getDate(date: Date, delimiter: string = "-"): string {
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
    },
    loadNextTen() {
      this.showLoadNextButton = false;
      this.showLoading = true;
      this.$server.get(
        "/api/logue?method=limit&limit=" + this.limitStart + ",10",
        r => {
          if (Array.isArray(r.data) && r.data.length > 0) {
            let data = r.data;
            let arr: Array<LogueArrayItem> = this.monologue;
            arr.forEach(k => {
              data.forEach((e, i) => {
                let logueItem = {
                  id: e.id,
                  title: e.title,
                  contents: e.contents,
                  type: e.type,
                  time: e.date.split(" ")[1]
                };
                if (e.date.split(" ")[0] == k.date) {
                  k.logue.push(logueItem);
                } else {
                  arr.push({
                    date: e.date.split(" ")[0],
                    logue: [logueItem]
                  });
                }
              });
            });
            this.showLoadNextButton = r.data.length == 10;
          } else {
            this.showLoadNextButton = false;
          }
        }
      );
      this.showLoading = false;
      this.limitStart += 10;
    }
  },
  watch: {
    targetDate(v) {
      this.gotoDate();
    }
  },
  mounted() {
    this.$server.get("/api/logue?method=limit&limit=0,10", r => {
      if (Array.isArray(r.data) && r.data.length > 0) {
        (this.monologue as Array<LogueArrayItem>) = this.getArray(r.data);
      } else {
        this.empty = true;
      }
    });
    this.$server.get("/api/data?comp=logue&name=length", r => {
      if (Number.isInteger(r.data)) {
        this.total = r.data;
        if (this.total > 10) {
          this.showLoadNextButton = true;
        }
      }
    });
    this.$server.post(
      "/api/auth",
      {
        method: "auth"
      },
      r => {
        this.auth = r.data;
      }
    );
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
  @media screen and (max-width: 1024px) {
    display: none;
  }
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
  display: none;
}

.date-info {
  .date {
    &::selection {
      background-color: transparent;
    }
  }
}

.home {
  height: 100%;
  position: relative;
}

.load-more-button,
.loading {
  display: block;
  margin: auto;
  margin-top: 56px;
  margin-bottom: 72px;
}
</style>