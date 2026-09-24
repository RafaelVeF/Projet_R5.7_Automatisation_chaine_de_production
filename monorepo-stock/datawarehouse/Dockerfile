FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY Datawarehouse.csproj ./
RUN dotnet restore Datawarehouse.csproj

COPY . .
RUN dotnet publish Datawarehouse.csproj -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app

EXPOSE 8080
COPY --from=build /app/publish .

ENTRYPOINT ["dotnet", "Datawarehouse.dll"]
