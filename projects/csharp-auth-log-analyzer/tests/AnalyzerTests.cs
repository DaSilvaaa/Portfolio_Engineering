using Xunit;

public class AnalyzerTests
{
    [Fact]
    public void DetectsBruteForceWithinWindow()
    {
        var lines = Enumerable.Range(0, 6)
            .Select(i => $"Oct  3 12:00:{i:00} host sshd[1]: Failed password for root from 10.0.0.5 port 22 ssh2");
        var r = Analyzer.Detect(lines, 5, TimeSpan.FromSeconds(60), 2026).ToList();
        Assert.Single(r);
        Assert.Equal("10.0.0.5", r[0].Ip);
        Assert.Equal(6, r[0].Failures);
    }

    [Fact]
    public void IgnoresSlowAttempts()
    {
        var lines = Enumerable.Range(0, 5)
            .Select(i => $"Oct  3 12:{i * 10:00}:00 host sshd[1]: Failed password for root from 10.0.0.9 port 22 ssh2");
        Assert.Empty(Analyzer.Detect(lines, 5, TimeSpan.FromSeconds(60), 2026));
    }
}