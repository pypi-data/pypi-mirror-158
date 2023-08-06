import { ac as ordered_colors } from './index.50dc598e.js';

const get_next_color = (index) => {
  return ordered_colors[index % ordered_colors.length];
};

export { get_next_color as g };
