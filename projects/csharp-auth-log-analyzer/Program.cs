using System.Text.Json;

var path = args.Length > 0 ? args[0] : "auth.log";
var threshold = args.Length > 1 ? int.Parse(args[1]) : 5;
var windowSec = args.Length > 2 ? int.Parse(args[2]) : 60;

var result = Analyzer
    .Detect(File.ReadLines(path), threshold, TimeSpan.FromSeconds(windowSec), DateTime.UtcNow.Year)
    .OrderByDescending(o => o.Failures)
    .ToList();

Console.WriteLine(JsonSerializer.Serialize(result, new JsonSerializerOptions { WriteIndented = true }));
return result.Count > 0 ? 1 : 0;