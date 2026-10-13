using System.Globalization;
using System.Text.RegularExpressions;

public record Offender(string Ip, int Failures, DateTime First, DateTime Last, List<string> Users);

public static class Analyzer
{
    private static readonly Regex Rx = new(
        @"^(?<ts>\w{3}\s+\d+\s[\d:]{8}).*Failed password for (invalid user )?(?<user>\S+) from (?<ip>\d+\.\d+\.\d+\.\d+)",
        RegexOptions.Compiled);

    public static IEnumerable<Offender> Detect(IEnumerable<string> lines, int threshold, TimeSpan window, int year)
    {
        var byIp = new Dictionary<string, List<(DateTime t, string user)>>();

        foreach (var line in lines)
        {
            var m = Rx.Match(line);
            if (!m.Success) continue;
            var ts = Regex.Replace(m.Groups["ts"].Value, @"\s+", " ") + " " + year;
            if (!DateTime.TryParseExact(ts, "MMM d HH:mm:ss yyyy", CultureInfo.InvariantCulture,
                    DateTimeStyles.None, out var t)) continue;
            var ip = m.Groups["ip"].Value;
            if (!byIp.TryGetValue(ip, out var list)) byIp[ip] = list = new();
            list.Add((t, m.Groups["user"].Value));
        }

        foreach (var (ip, ev) in byIp)
        {
            ev.Sort((a, b) => a.t.CompareTo(b.t));
            int best = 0, bestStart = 0, bestEnd = 0, lo = 0;
            for (int hi = 0; hi < ev.Count; hi++)
            {
                while (ev[hi].t - ev[lo].t > window) lo++;
                if (hi - lo + 1 > best) { best = hi - lo + 1; bestStart = lo; bestEnd = hi; }
            }
            if (best >= threshold)
                yield return new Offender(ip, best, ev[bestStart].t, ev[bestEnd].t,
                    ev.Skip(bestStart).Take(bestEnd - bestStart + 1).Select(e => e.user).Distinct().ToList());
        }
    }
}