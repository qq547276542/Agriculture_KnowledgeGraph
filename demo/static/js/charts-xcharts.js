(function () {
var data = [{"xScale":"ordinal","comp":[],"main":[{"className":".main.l1","data":[{"y":15,"x":"2012-11-19T00:00:00"},{"y":11,"x":"2012-11-20T00:00:00"},{"y":8,"x":"2012-11-21T00:00:00"},{"y":10,"x":"2012-11-22T00:00:00"},{"y":1,"x":"2012-11-23T00:00:00"},{"y":6,"x":"2012-11-24T00:00:00"},{"y":8,"x":"2012-11-25T00:00:00"}]},{"className":".main.l2","data":[{"y":29,"x":"2012-11-19T00:00:00"},{"y":33,"x":"2012-11-20T00:00:00"},{"y":13,"x":"2012-11-21T00:00:00"},{"y":16,"x":"2012-11-22T00:00:00"},{"y":7,"x":"2012-11-23T00:00:00"},{"y":18,"x":"2012-11-24T00:00:00"},{"y":8,"x":"2012-11-25T00:00:00"}]}],"type":"line-dotted","yScale":"linear"},{"xScale":"ordinal","comp":[],"main":[{"className":".main.l1","data":[{"y":12,"x":"2012-11-19T00:00:00"},{"y":18,"x":"2012-11-20T00:00:00"},{"y":8,"x":"2012-11-21T00:00:00"},{"y":7,"x":"2012-11-22T00:00:00"},{"y":6,"x":"2012-11-23T00:00:00"},{"y":12,"x":"2012-11-24T00:00:00"},{"y":8,"x":"2012-11-25T00:00:00"}]},{"className":".main.l2","data":[{"y":29,"x":"2012-11-19T00:00:00"},{"y":33,"x":"2012-11-20T00:00:00"},{"y":13,"x":"2012-11-21T00:00:00"},{"y":16,"x":"2012-11-22T00:00:00"},{"y":7,"x":"2012-11-23T00:00:00"},{"y":18,"x":"2012-11-24T00:00:00"},{"y":8,"x":"2012-11-25T00:00:00"}]}],"type":"cumulative","yScale":"linear"},{"xScale":"ordinal","comp":[],"main":[{"className":".main.l1","data":[{"y":12,"x":"2012-11-19T00:00:00"},{"y":18,"x":"2012-11-20T00:00:00"},{"y":8,"x":"2012-11-21T00:00:00"},{"y":7,"x":"2012-11-22T00:00:00"},{"y":6,"x":"2012-11-23T00:00:00"},{"y":12,"x":"2012-11-24T00:00:00"},{"y":8,"x":"2012-11-25T00:00:00"}]},{"className":".main.l2","data":[{"y":29,"x":"2012-11-19T00:00:00"},{"y":33,"x":"2012-11-20T00:00:00"},{"y":13,"x":"2012-11-21T00:00:00"},{"y":16,"x":"2012-11-22T00:00:00"},{"y":7,"x":"2012-11-23T00:00:00"},{"y":18,"x":"2012-11-24T00:00:00"},{"y":8,"x":"2012-11-25T00:00:00"}]}],"type":"bar","yScale":"linear"}];
var order = [0, 1, 0, 2],
  i = 0,
  xFormat = d3.time.format('%A'),
  chart = new xChart('line-dotted', data[order[i]], '#chart', {
    axisPaddingTop: 5,
    dataFormatX: function (x) {
      return new Date(x);
    },
    tickFormatX: function (x) {
      return xFormat(x);
    },
    timing: 1250
  }),
  rotateTimer,
  toggles = d3.selectAll('.multi button'),
  t = 3500;

function updateChart(i) {
  var d = data[i];
  chart.setData(d);
  toggles.classed('toggled', function () {
    return (d3.select(this).attr('data-type') === d.type);
  });
  return d;
}

toggles.on('click', function (d, i) {
  clearTimeout(rotateTimer);
  updateChart(i);
});

function rotateChart() {
  i += 1;
  i = (i >= order.length) ? 0 : i;
  var d = updateChart(order[i]);
  rotateTimer = setTimeout(rotateChart, t);
}
rotateTimer = setTimeout(rotateChart, t);
}());

(function () {
      
      var data = {
  "xScale": "ordinal",
  "yScale": "linear",
  "main": [
    {
      "className": ".pizza",
      "data": [
        {
          "x": "Pepperoni",
          "y": 4
        },
        {
          "x": "Cheese",
          "y": 8
        }
      ]
    }
  ]
};
      var myChart = new xChart('bar', data, '#example1');
      
    }());

(function () {
      
      var data = {
  "xScale": "ordinal",
  "yScale": "linear",
  "main": [
    {
      "className": ".pizza",
      "data": [
        {
          "x": "Pepperoni",
          "y": 4
        },
        {
          "x": "Cheese",
          "y": 8
        }
      ]
    },
    {
      "className": ".pizza",
      "data": [
        {
          "x": "Pepperoni",
          "y": 6
        },
        {
          "x": "Cheese",
          "y": 5
        }
      ]
    }
  ]
};
      var myChart = new xChart('bar', data, '#example2');
      
    }());

(function () {
      
      var data = {
  "xScale": "time",
  "yScale": "linear",
  "type": "line",
  "main": [
    {
      "className": ".pizza",
      "data": [
        {
          "x": "2012-11-05",
          "y": 1
        },
        {
          "x": "2012-11-06",
          "y": 6
        },
        {
          "x": "2012-11-07",
          "y": 13
        },
        {
          "x": "2012-11-08",
          "y": -3
        },
        {
          "x": "2012-11-09",
          "y": -4
        },
        {
          "x": "2012-11-10",
          "y": 9
        },
        {
          "x": "2012-11-11",
          "y": 6
        }
      ]
    }
  ]
};
      var opts = {
  "dataFormatX": function (x) { return d3.time.format('%Y-%m-%d').parse(x); },
  "tickFormatX": function (x) { return d3.time.format('%A')(x); }
};
      
      var myChart = new xChart('line', data, '#example3', opts);
      
    }());

(function () {
      var tt = document.createElement('div'),
  leftOffset = -(~~$('html').css('padding-left').replace('px', '') + ~~$('body').css('margin-left').replace('px', '')),
  topOffset = -32;
tt.className = 'ex-tooltip';
document.body.appendChild(tt);

      var data = {
  "xScale": "time",
  "yScale": "linear",
  "main": [
    {
      "className": ".pizza",
      "data": [
        {
          "x": "2012-11-05",
          "y": 6
        },
        {
          "x": "2012-11-06",
          "y": 6
        },
        {
          "x": "2012-11-07",
          "y": 8
        },
        {
          "x": "2012-11-08",
          "y": 3
        },
        {
          "x": "2012-11-09",
          "y": 4
        },
        {
          "x": "2012-11-10",
          "y": 9
        },
        {
          "x": "2012-11-11",
          "y": 6
        }
      ]
    }
  ]
};
      var opts = {
  "dataFormatX": function (x) { return d3.time.format('%Y-%m-%d').parse(x); },
  "tickFormatX": function (x) { return d3.time.format('%A')(x); },
  "mouseover": function (d, i) {
    var pos = $(this).offset();
    $(tt).text(d3.time.format('%A')(d.x) + ': ' + d.y)
      .css({top: topOffset + pos.top, left: pos.left + leftOffset})
      .show();
  },
  "mouseout": function (x) {
    $(tt).hide();
  }
};
      
      var myChart = new xChart('line-dotted', data, '#example4', opts);
      
    }());

(function () {
      var errorBar = {
        enter: function (self, storage, className, data, callbacks) {
          var insertionPoint = xChart.visutils.getInsertionPoint(9),
            container,
            eData = data.map(function (d) {
              d.data = d.data.map(function (d) {
                return [{x: d.x, y: d.y - d.e}, {x: d.x, y: d.y}, {x: d.x, y: d.y + d.e}];
              });
              return d;
            }),
            paths;

          container = self._g.selectAll('.errorLine' + className)
            .data(eData, function (d) {
              return d.className;
            });

          container.enter().insert('g', insertionPoint)
            .attr('class', function (d, i) {
              return 'errorLine' + className.replace(/\./g, ' ') + ' color' + i;
            });

          paths = container.selectAll('path')
            .data(function (d) {
              return d.data;
            }, function (d) {
              return d[0].x;
            });

          paths.enter().insert('path')
            .style('opacity', 0)
            .attr('d', d3.svg.line()
              .x(function (d) {
                return self.xScale(d.x) + self.xScale.rangeBand() / 2;
              })
              .y(function (d) { return self.yScale(d.y); })
            );

          storage.containers = container;
          storage.paths = paths;
        },
        update: function (self, storage, timing) {
          storage.paths.transition().duration(timing)
            .style('opacity', 1)
            .attr('d', d3.svg.line()
              .x(function (d) {
                return self.xScale(d.x) + self.xScale.rangeBand() / 2;
              })
              .y(function (d) { return self.yScale(d.y); })
            );
        },
        exit: function (self, storage, timing) {
          storage.paths.exit()
            .transition().duration(timing)
            .style('opacity', 0);
        },
        destroy: function (self, storage, timing) {
          storage.paths.transition().duration(timing)
            .style('opacity', 0)
            .remove();
        }
      };

      xChart.setVis('error', errorBar);

      var data = [{
          "xScale": "ordinal",
          "yScale": "linear",
          "main": [
            {
              "className": ".errorExample",
              "data": [
                {
                  "x": "Ponies",
                  "y": 12
                },
                {
                  "x": "Unicorns",
                  "y": 23
                },
                {
                  "x": "Trolls",
                  "y": 1
                }
              ]
            }
          ],
          "comp": [
            {
              "type": "error",
              "className": ".comp.errorBar",
              "data": [
                {
                  "x": "Ponies",
                  "y": 12,
                  "e": 5
                },
                {
                  "x": "Unicorns",
                  "y": 23,
                  "e": 2
                },
                {
                  "x": "Trolls",
                  "y": 1,
                  "e": 1
                }
              ]
            }
          ]
        },
        {
          "xScale": "ordinal",
          "yScale": "linear",
          "main": [
            {
              "className": ".errorExample",
              "data": [
                {
                  "x": "Ponies",
                  "y": 76
                },
                {
                  "x": "Unicorns",
                  "y": 45
                },
                {
                  "x": "Trolls",
                  "y": 82
                }
              ]
            }
          ],
          "comp": [
            {
              "type": "error",
              "className": ".comp.errorBar",
              "data": [
                {
                  "x": "Ponies",
                  "y": 76,
                  "e": 12
                },
                {
                  "x": "Unicorns",
                  "y": 45,
                  "e": 3
                },
                {
                  "x": "Trolls",
                  "y": 82,
                  "e": 12
                }
              ]
            }
          ]
        }
      ];

      var myChart = new xChart('bar', data[0], '#exampleVis'),
        i = 0;

      function timer() {
        setTimeout(function () {
          timer();
          i += 1;
          myChart.setData(data[i % 2]);
        }, 3000);
      }
      timer();
    }());