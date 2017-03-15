frappe.provide("frappe.ui");

frappe.ui.Chart = Class.extend({
	init: function(opts) {
		this.opts = {};
		$.extend(this.opts, opts);
		this.show_chart(false);

		$(this.opts.wrapper).html('<button class="btn btn-default btn-xs show-hide-chart" ' +
			'type="button" style="margin: 10px;">' +
			'<span class="chart-btn-text">Show chart </span>' +
			'<span class="chart-chevron octicon collapse-indicator octicon-chevron-down"' +
				'style="font-size: inherit;"></span></button>' +
			'<div class="chart_area_result" style="padding-bottom: 10px">' +
			'</div>');
		
		this.setup_events();
		
		this.opts.bind_to = frappe.dom.set_unique_id(this.opts.wrapper.find(".chart_area_result"));

		if(this.opts.data && ((this.opts.data.columns && this.opts.data.columns.length >= 1)
			|| (this.opts.data.rows && this.opts.data.rows.length >= 1))) {
				this.chart = this.render_chart();
				this.show_chart(true);
		}

		return this.chart;
	},

	render_chart: function() {
		var chart_dict = {
			bindto: '#' + this.opts.bind_to,
		    data: {},
			axis: {
		        x: {
		            type: 'category' // this needed to load string x value
		        },
				y: {
					padding: { bottom: 10 }
				}
			},
			padding: {
				left: 60,
				top: 30,
				right: 30,
				bottom: 10
			},
			pie: {
				expand : false
			},
			bar: {
				"width": 10
			}
		};

		$.extend(chart_dict, this.opts);

		chart_dict["data"]["type"] = this.opts.chart_type || "line";

		return c3.generate(chart_dict);
	},

	show_chart: function(show) {
		this.opts.wrapper.toggle(show);
	},

	set_chart_size: function(width, height) {
		this.chart.resize({
			width: width,
			height: height
		});
	},
	
	setup_events: function(){
		var me = this;
		var chart_result = me.opts.wrapper.find(".chart_area_result");
		
		chart_result.toggle(false);
		me.opts.wrapper.find(".show-hide-chart").toggle(true).on("click", function(){
			
			if ($(this).find(".chart-btn-text").text()==__("Show chart ")) {
				chart_result.toggle(true);
				$(this).find(".chart-btn-text").text(__("Hide "));
				$(this).find(".chart-chevron").removeClass("octicon-chevron-down").addClass("octicon-chevron-up");
			}
			else {
				chart_result.toggle(false);
				$(this).find(".chart-btn-text").text(__("Show chart "));
				$(this).find(".chart-chevron").removeClass("octicon-chevron-up").addClass("octicon-chevron-down");
			}
		});
	}
});
