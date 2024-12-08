export default function format_time(time_in_seconds: number) {
  const minutes = Math.floor(time_in_seconds / 60)
  const seconds = (time_in_seconds % 60).toFixed(0)
  return `${minutes}:${parseInt(seconds) < 10 ? '0' : ''}${seconds}`
}
