class Pgram < Formula
  desc "Pangram AI-detection CLI with local scan history and a result cache"
  homepage "https://github.com/lucasheriques/pgram"
  version "0.1.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/lucasheriques/pgram/releases/download/v0.1.0/pgram_0.1.0_darwin_arm64.tar.gz"
      sha256 "61f0644fb3f5f6e05b2ceab2fb7b0f7701b4b9f7e87fc4fcde301bb67c114185"
    end
    on_intel do
      url "https://github.com/lucasheriques/pgram/releases/download/v0.1.0/pgram_0.1.0_darwin_amd64.tar.gz"
      sha256 "a4f05226fa53842e3a7783e9fa13b1ade94301f3b00d713c4d1a0e45f1fa07ba"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/lucasheriques/pgram/releases/download/v0.1.0/pgram_0.1.0_linux_arm64.tar.gz"
      sha256 "9e2f8b070744409314f47cc403b068e84513255d59e03765130b58a59060421f"
    end
    on_intel do
      url "https://github.com/lucasheriques/pgram/releases/download/v0.1.0/pgram_0.1.0_linux_amd64.tar.gz"
      sha256 "4b1fb8fabfb6e930f1973d7ca47be5494a2f5ec5b0ead2293630eb0fac262579"
    end
  end

  def install
    bin.install "pgram"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/pgram version")
  end
end
