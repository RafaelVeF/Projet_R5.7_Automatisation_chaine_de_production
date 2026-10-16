var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

app.MapGet("/health", () => Results.Ok(new { status = "ok", service = "datawarehouse" }));

app.MapGet("/api/stocks", () => Results.Ok(new[]
{
    new { id = 1, code = "SAMPLE-001", designation = "Article Test", quantite = 100 }
}));

app.Run();