<template>
	<div class="home" :class="auth ? '' : 'unauthed'">
		<div class="mono-main">
			<div v-if="!empty && loadingPage" class="loading">
				<md-progress-spinner md-mode="indeterminate" />
			</div>
			<md-empty-state v-if="empty && !loadingPage">
				<span class="md-empty-state-icon mdi mdi-help-circle-outline" />
				<span class="md-empty-state-label">空页面</span>
				<span class="md-empty-state-description">此页面目前没有任何内容</span>
			</md-empty-state>
			<div v-if="!empty && !loadingPage">
				<md-button :style="{ opacity: backToTopButtonOpacity }" @click="toTop()" class="speeddial desktop md-primary">返回顶部</md-button>
				<md-speed-dial class="speeddial mobile" :style="{ opacity: backToTopButtonOpacity }">
					<md-speed-dial-target class="md-primary" @click="toTop()">
						<md-icon class="mdi mdi-chevron-up" />
					</md-speed-dial-target>
				</md-speed-dial>
				<md-button class="datepicker-button desktop md-primary md-raised md-icon-button" @click="openDatePicker()">
					<md-icon class="mdi mdi-calendar" />
				</md-button>
				<md-button class="datepicker-button mobile md-primary md-icon-button" @click="openDatePicker()">
					<md-icon class="mdi mdi-calendar" />
				</md-button>
				<div class="datepicker-container">
					<md-datepicker ref="picker" class="datepicker" v-model="targetDate" :md-immediately="true" />
				</div>
				<div v-for="(i, k) in monologue" :key="k" class="logue">
					<div class="meta">
						<span class="date-info">
							<span class="mdi calendar" />
							<a :href="'#' + i.date" :id="i.date" :name="i.date" class="date">{{ getDateString(i.date) }}</a>
						</span>
					</div>
					<div class="content" v-for="(a, b) in i.logue" :key="b">
						<div class="status-info" :class="getColorByType(a.type)">
							<span class="status" :class="getIconByType(a.type)">
								<span @click="getLogueDialog(a.id, a.title, a.contents, a.type)" :id="a.id" class="title">{{ a.title }}</span>
							</span>
						</div>
						<div class="logue">
							<div class="tools">
								<span v-if="auth" class="edit action-span" @click="$router.push({ name: 'admin-edit-event', params: { id: a.id } })">编辑</span>
								<span
									v-if="auth"
									class="delete action-span"
									@click="
										targetID = a.id;
										deleteConfirmDialog = true;
									"
									>删除</span
								>
								<span @click="copyLogueLink(a.id)" class="id action-span">#{{ a.id }}</span>
							</div>
							<div class="logue-content" v-html="a.contents"></div>
						</div>
					</div>
				</div>
			</div>
			<div class="load-more">
				<md-button v-if="showLoadNextButton && !loadingPage" @click="loadNextTen()" class="md-primary md-raised load-more-button">加载更多</md-button>
				<md-progress-spinner md-mode="indeterminate" v-if="showLoading" class="loading-block" />
			</div>
			<md-dialog v-if="auth" :md-active.sync="deleteConfirmDialog">
				<md-dialog-title>删除确认</md-dialog-title>
				<md-dialog-content>是否要确认删除此事件？此操作无法回滚。</md-dialog-content>
				<md-dialog-actions>
					<md-button
						@click="
							deleteEvent();
							deleteConfirmDialog = false;
						"
						class="md-primary"
						>确认删除</md-button
					>
					<md-button @click="deleteConfirmDialog = false" class="md-primary md-raised">取消</md-button>
				</md-dialog-actions>
			</md-dialog>
			<md-dialog :md-active="logueDialog">
				<md-dialog-content>
					<div class="event-detail">
						<div class="title">
							<h1 :class="getColorByType(selectedType)">
								{{ selectedTitle }}
								<span class="id">#{{ selectedID }}</span>
							</h1>
						</div>
						<div v-html="selectedContents" class="content typo" :class="getColorByType(selectedType)"></div>
					</div>
				</md-dialog-content>
				<md-dialog-actions>
					<md-button @click="logueDialog = false" class="md-primary">知道了</md-button>
				</md-dialog-actions>
			</md-dialog>
			<md-snackbar :md-active.sync="snackbar" md-postion="center" md-persistent :md-duration="1500"> {{ snackbarMessage }}</md-snackbar>
			<md-dialog :md-active.sync="loadingDialog">
				<md-dialog-content class="loading-dialog-content">
					<md-progress-spinner md-mode="indeterminate" class="loading-dialog-spinner" />
				</md-dialog-content>
			</md-dialog>
			<md-dialog class="firsttime-dialog" :md-active.sync="firstTimeDialog">
				<md-dialog-content>
					<md-steppers :md-active-step.sync="firstTimeActiveStep" :md-vertical="!isPC()" :md-linear="isPC()">
						<md-step class="firsttime-step" :id="firstTimeSteps[0]" md-label="欢迎" md-description="让我们开始吧">
							<md-empty-state>
								<img src="../assets/block.png" class="firsttime-logo" />
								<span class="md-empty-state-label">欢迎</span>
								<span class="md-empty-state-description">仅需几步即可了解此网站</span>
							</md-empty-state>
						</md-step>
						<md-step class="firsttime-step" :id="firstTimeSteps[1]" md-label="日期访问" md-description="用日期快速查找">
							<div class="title">
								<md-icon class="mdi mdi-calendar" />
								<h1>日期访问</h1>
							</div>
							<p>
								看到右上角的
								<md-icon class="mdi mdi-calendar" /> 了吗？那个是日期选择器。点击它，即可选择一个日期。如果此日期当天有过更新，则会跳转到这个日期的位置。
							</p>
							<p v-if="isPC()">
								你可以通过
								<kbd>Ctrl</kbd> + <kbd>G</kbd> 组合键快速唤出它。
							</p>
						</md-step>
						<md-step class="firsttime-step" :id="firstTimeSteps[2]" md-label="分享事件" md-description="获取某个事件的特定链接">
							<div class="title">
								<md-icon class="mdi mdi-share-variant" />
								<h1>分享事件</h1>
							</div>
							<p>
								如果想要获取属于某一特定事件的链接，可以{{ isPC() ? "将鼠标移动至一个请求上方" : "点击该请求所在区域" }}，随即会出现一个类似于
								<span style="font-weight: bold; color: #aaa">#1</span> 的标识。
							</p>
							<p>点击标识即可复制链接，当他人访问该链接时，第一时间将会展示出此事件。</p>
						</md-step>
						<md-step class="firsttime-step" :id="firstTimeSteps[3]" md-label="管理后台" md-description="管理页面">
							<div class="title">
								<md-icon class="mdi mdi-cogs" />
								<h1>管理后台</h1>
							</div>
							<p>管理后台可以协助网站管理者对内容进行管理。登录之后，你将获取一个用户标识，利用此用户标识可以创建、编辑新的事件、投票、表单等内容。</p>
							<p>管理后台有密码保护。</p>
						</md-step>
					</md-steppers>
				</md-dialog-content>
				<md-dialog-actions>
					<md-button v-if="firstTimeActiveStep === 'firsttime-first'" class="md-primary" @click="firstTimeDialog = false">不了</md-button>
					<md-button class="md-primary md-raised" @click="nextStep()">
						{{ firstTimeActiveStep === "firsttime-first" ? "开始吧" : firstTimeSteps.indexOf(firstTimeActiveStep) === firstTimeSteps.length - 1 ? "结束" : "继续" }}
					</md-button>
				</md-dialog-actions>
			</md-dialog>
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
// @ts-ignore
import MdSnackbar from "vue-material/dist/components/MdSnackbar";
// @ts-ignore
import MdSteppers from "vue-material/dist/components/MdSteppers";
import { copy, isNumericString, isPC } from "@/functions";
import { setcookie, getcookie } from '@/cookie';

Vue.use(MdButton)
	.use(MdDialog)
	.use(MdDatepicker)
	.use(MdContent)
	.use(MdSpeedDial)
	.use(MdIcon)
	.use(MdEmptyState)
	.use(MdProgress)
	.use(MdSnackbar)
	.use(MdSteppers);

export default Vue.extend({
	data() {
		return {
			monologue: [],
			datePickDialog: false,
			targetDate: "",
			empty: false,
			auth: false,
			limitStart: 10,
			showLoadNextButton: false,
			showLoading: false,
			total: 0,
			backToTopButtonOpacity: 0,
			targetID: -1,
			deleteConfirmDialog: false,
			snackbarMessage: "",
			snackbar: false,
			selectedID: -1,
			selectedTitle: "",
			selectedContents: "",
			selectedType: "",
			logueDialog: false,
			loadingPage: true,
			loadedLogueID: [],
			hashContent: "",
			loadingDialog: false,
			firstTimeDialog: false,
			firstTimeActiveStep: "firsttime-first",
			firstTimeSteps: ["firsttime-first", "firsttime-second", "firsttime-third", "firsttime-fourth"]
		};
	},
	methods: {
		isPC,
		nextStep() {
			if (this.firstTimeSteps.indexOf(this.firstTimeActiveStep) === this.firstTimeSteps.length - 1) {
				this.firstTimeDialog = false;
				return;
			}
			let targetIndex = this.firstTimeSteps.indexOf(this.firstTimeActiveStep) + 1;
			this.firstTimeActiveStep = this.firstTimeSteps[targetIndex];
		},
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
			let monthMatch = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
			let month = monthMatch[date.getMonth()];
			let day = date.getDate();
			let year = date.getFullYear();
			return `${month} ${day}, ${year}`;
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
		gotoID(id: number) {
			location.hash = id.toString();
		},
		copyLogueLink(id: number) {
			let link = location.protocol + "//" + location.host + "/#" + id.toString();
			copy(link, () => {
				this.snackbarMessage = "成功复制当前事件链接";
				this.snackbar = true;
			});
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
			locale.dateFormat = "yyyy-MM-dd";
			locale.days = ["星期天", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
			locale.shortDays = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"];
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
			this.$server.get("/api/logue?method=limit&limit=" + this.limitStart + ",10", r => {
				if (Array.isArray(r.data) && r.data.length > 0) {
					let data = r.data;
					let arr: Array<LogueArrayItem> = this.monologue;
					let dateBefore = "";
					let ix = -1;
					arr.forEach((k, t) => {
						data.forEach((e, i) => {
							let logueItem = {
								id: e.id,
								title: e.title,
								contents: e.contents,
								type: e.type,
								time: e.date.split(" ")[1]
							};
							console.log(e.date.split(" ")[0], k.date);
							if (e.date.split(" ")[0] === k.date) {
								k.logue.push(logueItem);
							} else if (e.date.split(" ")[0] === dateBefore) {
								arr[ix - 1].logue.push(logueItem);
							} else {
								dateBefore = e.date.split(" ")[0];
								ix = arr.push({
									date: e.date.split(" ")[0],
									logue: [logueItem]
								});
							}
						});
					});
					this.showLoadNextButton = r.data.length == 10;
					this.backToTopButtonOpacity = 1;
					console.log(arr);
				} else {
					this.showLoadNextButton = false;
				}
			});
			this.showLoading = false;
			this.limitStart += 10;
		},
		toTop() {
			window.scrollTo(0, 0);
		},
		getSnackbar(message: string) {
			this.snackbarMessage = message;
			this.snackbar = !this.snackbar;
		},
		deleteEvent() {
			this.$server.post(
				"/api/logue",
				{
					method: "delete",
					id: this.targetID
				},
				r => {
					if (r.data) {
						this.getSnackbar("成功删除 #" + this.targetID + " 事件，即将为您刷新。");
						setTimeout(() => {
							this.$router.go(0);
						}, 1500);
					} else {
						this.getSnackbar("出错了！暂时无法删除此事件。");
					}
					this.targetID = -1;
				}
			);
		},
		getLogueDialog(id: number, title: string, contents: string, type: string) {
			this.selectedID = id;
			this.selectedTitle = title;
			this.selectedContents = contents;
			this.selectedType = type;
			this.logueDialog = true;
		},
		handleIDAccess() {
			let hash = this.hashContent;
			let alreadyIn = false;
			if (!isNumericString(hash)) {
				return false;
			} else {
				// filter
				/* (this.monologue as Array<LogueArrayItem>).forEach(k => {
                    k.logue.forEach(t => {
                        if (t.id.toString() === hash) {
                            alreadyIn = true;
                        }
                    });
                });
                if (!alreadyIn) { */
				this.logueDialog = false;
				this.loadingDialog = true;
				this.$server.get("/api/logue?method=id&id=" + hash, r => {
					this.loadingDialog = false;
					if (r.data) {
						let data = r.data;
						this.getLogueDialog(data.id, data.title, data.contents, data.type);
					}
				});
				/* } */
				return;
			}
		}
	},
	watch: {
		targetDate(v) {
			if (this.targetDate === this.getDate(new Date())) {
				return false;
			}
			this.gotoDate();
		},
		monologue(v: Array<LogueArrayItem>) {
			v.forEach(k => {
				let date = k.date;
				k.logue = k.logue.slice().sort((a, b) => {
					return new Date(date + " " + b.time).getTime() - new Date(date + " " + a.time).getTime();
				});
			});
		},
		$route(to, from) {
			if (to.name === "home") {
				this.hashContent = to.hash.slice(1);
				this.handleIDAccess();
			}
		}
	},
	created() {
		// default load
		this.$server.get("/api/logue?method=limit&limit=0,10", r => {
			if (Array.isArray(r.data) && r.data.length > 0) {
				(this.monologue as Array<LogueArrayItem>) = this.getArray(r.data);
			} else {
				this.empty = true;
			}
			this.loadingPage = false;
		});
		// load more
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
		this.hashContent = location.hash.includes("?") ? location.hash.slice(1, location.hash.indexOf("?")) : location.hash.slice(1);
	},
	mounted() {
		this.handleIDAccess();
		if (getcookie("ft") === undefined) {
			setcookie("ft", "false");
			this.firstTimeDialog = true;
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

.datepicker-container {
	height: 0 !important;
}

.datepicker-button {
	@media screen and (min-width: 1024px) {
		position: absolute;
		&.mobile {
			display: none;
		}
	}
	@media screen and (max-width: 1024px) {
		position: fixed;
		&.desktop {
			display: none;
		}
	}
	right: 16px;
	top: 16px;
}

.logue {
	box-sizing: content-box;
}

.speeddial.calendar {
	top: 32px;
	right: 32px;

	@media screen and (min-width: 1024px) {
		display: none;
	}
}

.speeddial {
	position: fixed;
	z-index: 1;
	transition: opacity 0.5s ease;
	bottom: 32px;
	right: 32px;

	@media screen and (max-width: 1024px) {
		&.desktop {
			display: none;
		}
	}

	@media screen and (min-width: 1024px) {
		&.mobile {
			display: none;
		}
	}
}

.datepicker {
	/*display: none;*/
	visibility: hidden;
	top: -100px;
	left: -100px;
	min-width: 0px;
	width: 0px;
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
.loading-block {
	display: block;
	margin: auto;
	margin-top: 56px;
	margin-bottom: 72px;
}

.event-detail {
	.title {
		text-align: left;
		line-height: 1.5;

		.blue {
			color: #2196f3;
		}

		.green {
			color: #4caf50;
		}

		.red {
			color: #f44336;
		}

		h1 {
			text-overflow: ellipsis;
			overflow: hidden;

			.id {
				width: 30px;
				color: #bbb;
				font-weight: normal;
				font-size: 18px;
			}
		}

		.icon {
			&.mdi-check {
				color: #4caf50;
			}

			&.mdi-information-outline {
				color: #2196f3;
			}

			&.mdi-alert {
				color: #f44336;
			}

			&::before {
				font-size: 30px;
			}
		}
	}
}

.loading-dialog-content {
	text-align: center;
	.loading-dialog-spinner {
		display: inline-flex;
	}
}

.firsttime-logo {
	width: 250px;
}
</style>
