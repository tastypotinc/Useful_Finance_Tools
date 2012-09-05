var stackgraph2 = new Grafico.StackGraph($('stackgraph2'),
{
  workload:       [8, 10,  6, 1,  7, 6, 9],
  your_workload:  [6,  8,  4, 1, 12, 6, 2],
  his_workload:   [2,  9, 12, 2,  8, 9, 8]
},
{
  markers :           "value",
  draw_axis :         false,
  plot_padding :      0,
  hover_text_color :  "#fff",
  background_color :  "#fff",
  datalabels: {
    workload:       "My workload",
    your_workload:  "Your workload",
    his_workload:   "His workload"
  }
});