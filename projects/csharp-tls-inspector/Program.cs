using System.Text.Json;

if (args.Length == 0)
{
    Console.Error.WriteLine("uso: TlsInspector <host[:porta]> [...]");
    return 2;
}

var reports = new List<object>();
var failed = false;

foreach (var target in args)
{
    var idx = target.LastIndexOf(':');
    var host = idx > 0 ? target[..idx] : target;
    var port = idx > 0 && int.TryParse(target[(idx + 1)..], out var p) ? p : 443;

    try
    {
        var (info, errors) = await Inspector.FetchAsync(host, port, TimeSpan.FromSeconds(8));
        var issues = CertRules.Evaluate(info, DateTime.UtcNow);

        if (errors != System.Net.Security.SslPolicyErrors.None)
            issues.Add($"validação da cadeia/nome falhou: {errors}");

        failed |= issues.Count > 0;
        reports.Add(new
        {
            host,
            port,
            info.Subject,
            info.NotAfter,
            Protocol = info.Protocol.ToString(),
            info.KeyAlgorithm,
            info.KeySize,
            info.SignatureAlgorithm,
            issues
        });
    }
    catch (Exception e)
    {
        failed = true;
        reports.Add(new { host, port, error = e.Message });
    }
}

Console.WriteLine(JsonSerializer.Serialize(reports, new JsonSerializerOptions { WriteIndented = true }));
return failed ? 1 : 0;