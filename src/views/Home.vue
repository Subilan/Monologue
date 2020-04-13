<template>
  <div class="home">
    <div class="mono-main">
      <div v-for="(i, k) in filter(monologue)" :key="k" class="logue">
        <div class="meta">
          <span class="status-icon" :class="getColorByType(i.type)">
            <span class="mdi" :class="getIconByType(i.type)" />
          </span>
          <span class="date">{{ i.date }}</span>
          <span class="badge latest" v-if="k === 0">latest</span>
        </div>
        <div class="content">
          <div class="logue-content">
            <h1 v-if="i.title">{{ i.title }}</h1>
            <p>{{ i.contents }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";

interface Logue {
  date: string;
  title?: string;
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
          title: "测试 1",
          type: "info",
          contents:
            "测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容测试内容"
        },
        {
          date: "2020/04/03",
          contents: "测试 3",
          type: "info"
        },
        {
          date: "2020/04/15",
          contents: "测试 2",
          type: "warning"
        },
        {
          date: "2020/04/01",
          contents: "测试 31",
          type: "solved"
        }
      ]
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
          info: "mdi-information-outline",
          warning: "mdi-alert-outline",
          solved: "mdi-check-circle-outline"
        },
        colorMatch: {
          info: "blue",
          warning: "red",
          solved: "green"
        }
      };
      return match[getType + "Match"][type];
    }
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
</style>