export function format_time(time_in_seconds: number) {
  const minutes = Math.floor(time_in_seconds / 60)
  const seconds = (time_in_seconds % 60).toFixed(0)
  return `${minutes}:${parseInt(seconds) < 10 ? '0' : ''}${seconds}`
}

export function cumulative_sum(arr: number[]) {
  return arr.reduce((a, x, i) => [...a, x + (a[i - 1] || 0)], [] as number[])
}
